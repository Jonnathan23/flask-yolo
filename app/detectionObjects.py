from dataclasses import dataclass
from typing import List, Optional
import cv2 as cv
import numpy as np

from app.data.db import OperationDetector, imageObjective

def implementLBP():
    print("Implementing LBP (Local Binary Patterns) for feature extraction.")
    
    
@dataclass
class MatchResult:
    found: bool                       # True  ⇒ se detectó el objeto
    goodMatches: Optional[List[cv.DMatch]] = None
    inlierMask: Optional[np.ndarray] = None
    homography: Optional[np.ndarray] = None


def implementSIFT(frame: np.ndarray) -> MatchResult:
    """
    Busca `imageObjective` en `frame`.  
    Si las coincidencias superan el umbral, devuelve MatchResult(found=True).
    De lo contrario, found=False.
    """
    # 1. Detectar–describir el frame
    sift = cv.SIFT_create(800, 3, 0.06, 10)
    kp_frame, desc_frame = sift.detectAndCompute(frame, None)
    if desc_frame is None:
        return MatchResult(found=False)

    # 2. RootSIFT en el frame
    cv.normalize(desc_frame, desc_frame, 1, 0, cv.NORM_L1)
    cv.sqrt(desc_frame, desc_frame)

    # 3. FLANN + ratio-test
    index_params  = dict(algorithm=1, trees=5)   # KD-Tree
    search_params = dict(checks=32)
    matcher = cv.FlannBasedMatcher(index_params, search_params)
    
    if (imageObjective.descriptors is None or imageObjective.descriptors.shape[0] < 2 or desc_frame.shape[0] < 2):
        # Muy pocos descriptores: saltamos este frame
        return MatchResult(found=False)

    raw = matcher.knnMatch(imageObjective.descriptors, desc_frame, k=2)
    ratio = 0.75
    good = [m for m, n in raw if m.distance < ratio * n.distance]

    # 4. Homografía vía RANSAC para validar geometría
    if len(good) < 10:
        return MatchResult(found=False)

    src = np.float32([imageObjective.keyPoints[m.queryIdx].pt for m in good])
    dst = np.float32([kp_frame[m.trainIdx].pt           for m in good])
    H, mask = cv.findHomography(src, dst, cv.RANSAC, 4.0)

    # 5. Decisión final
    # - parecido a tu C++: aceptamos si hay ≥70 coincidencias filtradas
    if H is not None and mask is not None and mask.sum() >= 70:
        print("encontrado")            # ⬅️  al estilo del enunciado
        return MatchResult(found=True, goodMatches=good, inlierMask=mask, homography=H)

    return MatchResult(found=False)


executeDetection = {
    OperationDetector.LBP: implementLBP,
    OperationDetector.SIFT: implementSIFT
}    