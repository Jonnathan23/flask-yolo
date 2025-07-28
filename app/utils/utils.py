import cv2 as cv
import time
from app.data.db import  operation, imageObjective


def drawSiftResults(result, frame, width, height, canvas):
    '''Dibuja los resultados de la detección SIFT en el canvas.'''
    # Sólo dibujamos cuando tenemos >70 goodMatches
    if len(result.goodMatches) > 70:
        # drawMatches entre logo e imagen actual
        matchVis = cv.drawMatches(
            imageObjective.image, imageObjective.keyPoints,
            frame,                    result.frameKeyPoints,
            result.goodMatches,       None,
            flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
        # ajustar tamaño al panel derecho
        matchVis = cv.resize(matchVis, (width, height))
        canvas[:, width*2:width*3] = matchVis
    else:
        canvas[:, width*2:width*3] = 0
    # si no llegan al umbral, mostramos sólo keypoints
    kpVis = cv.drawKeypoints(
        frame, result.frameKeyPoints, None,
        flags=cv.DrawMatchesFlags_DEFAULT
    )
    canvas[:, width:width*2] = kpVis
    