import cv2 as cv
import numpy as np

def upgradeImage(frame: np.ndarray) -> np.ndarray:
    # gris
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # desenfoque suave
    blur = cv.GaussianBlur(gray, (0,0), sigmaX=3, sigmaY=3)
    # unsharp mask
    sharpened = cv.addWeighted(gray, 1.5, blur, -0.5, 0)
    return sharpened