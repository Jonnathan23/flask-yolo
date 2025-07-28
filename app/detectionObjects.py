from dataclasses import dataclass
from typing import List, Optional
import cv2 as cv
import numpy as np

from app.classes.index import OperationDetector
from app.data.db import imageObjective, detector
from app.utils.filters import upgradeImage


def implementLBP(frame: np.ndarray):        
    faces = detector.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
    
    # Aplicar desenfoque gaussiano en cada ROI (sin máscara)
    for (x, y, w, h) in faces:
        roi = frame[y:y+h, x:x+w]
        blurred_roi = cv.GaussianBlur(roi, (31, 31), 0)
        frame[y:y+h, x:x+w] = blurred_roi
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Opcional    
    
    return frame
    
@dataclass
class MatchResult:
    found: bool
    frameKeyPoints: List[cv.KeyPoint]                     # ← siempre llenamos esto
    goodMatches: Optional[List[cv.DMatch]] = None
    inlierMask: Optional[np.ndarray]    = None
    homography: Optional[np.ndarray]    = None


sift = cv.SIFT_create(800, 3, 0.06, 10)

def implementSIFT(frame: np.ndarray) -> MatchResult:
    """
    Busca `imageObjective` en `frame`.  
    Si las coincidencias superan el umbral, devuelve MatchResult(found=True).
    De lo contrario, found=False.
    """
    
    frameUpgraged = upgradeImage(frame)
    kp_frame, desc_frame = sift.detectAndCompute(frameUpgraged, None)
    
    # si no hay descriptores, devolvemos sin keypoints
    if desc_frame is None or desc_frame.shape[0] < 2:
        return MatchResult(found=False, frameKeyPoints=kp_frame)

    # 2) RootSIFT y FLANN + ratio-test (igual que antes)
    cv.normalize(desc_frame, desc_frame, 1, 0, cv.NORM_L1)
    cv.sqrt(desc_frame, desc_frame)
    matcher = cv.FlannBasedMatcher(
        dict(algorithm=1, trees=5),
        dict(checks=32)
    )
    raw    = matcher.knnMatch(imageObjective.descriptors, desc_frame, k=2)
    good   = [m for m,n in raw if m.distance < 0.85 * n.distance]

    # 3) RANSAC homografía
    if len(good) < 10:
        return MatchResult(found=False, frameKeyPoints=kp_frame)

    src = np.float32([imageObjective.keyPoints[m.queryIdx].pt for m in good])
    dst = np.float32([kp_frame[m.trainIdx].pt           for m in good])
    H, mask = cv.findHomography(src, dst, cv.RANSAC, 4.0)

    # 4) decidimos “found” si hay suficientes inliers
    if H is not None and mask is not None and int(mask.sum()) >= 10:
        print(f"Encontrado {len(good)} coincidencias con homografía.")
        return MatchResult(
            found=True,
            frameKeyPoints=kp_frame,
            goodMatches=good,
            inlierMask=mask,
            homography=H
        )

    return MatchResult(found=False, frameKeyPoints=kp_frame)


executeDetection = {
    OperationDetector.LBP: implementLBP,
    OperationDetector.SIFT: implementSIFT
}    