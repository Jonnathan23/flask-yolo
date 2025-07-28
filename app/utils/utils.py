import cv2 as cv
import math
from typing import List, Tuple

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

    
def computeIoU(boxA: Tuple[int,int,int,int], boxB: Tuple[int,int,int,int]) -> float:
    """Compute Intersection over Union (IoU) of two boxes."""
    xA, yA, widthA, heightA = boxA; xB, yB, widthB, heightB = boxB
    x1, y1 = max(xA, xB), max(yA, yB); x2, y2 = min(xA+widthA, xB+widthB), min(yA+heightA, yB+heightB)
    if x2 <= x1 or y2 <= y1: return 0.0
    intersectionArea = (x2 - x1) * (y2 - y1)
    unionArea = widthA*heightA + widthB*heightB - intersectionArea
    return intersectionArea / unionArea

def filterAndMergeDetections(
    faces: List[Tuple[int,int,int,int]],
    iouThreshold: float = 0.4,
    distanceThresholdRatio: float = 0.5
) -> List[Tuple[int,int,int,int]]:
    # 1) Remove contained rectangles
    nonContained = [
        rect for rect in faces
        if not any(
            outer != rect
            and outer[0] <= rect[0] and outer[1] <= rect[1]
            and outer[0]+outer[2] >= rect[0]+rect[2]
            and outer[1]+outer[3] >= rect[1]+rect[3]
            for outer in faces
        )
    ]
    # 2) Cluster by IoU or center-distance
    unvisited = set(range(len(nonContained))); clusters = []
    while unvisited:
        idx = unvisited.pop(); component = {idx}; stack = [idx]
        while stack:
            current = stack.pop()
            for other in list(unvisited):
                boxA = nonContained[current]; boxB = nonContained[other]
                cxA, cyA = boxA[0]+boxA[2]/2, boxA[1]+boxA[3]/2
                cxB, cyB = boxB[0]+boxB[2]/2, boxB[1]+boxB[3]/2
                centerDistance = math.hypot(cxA-cxB, cyA-cyB)
                maxDim = max(boxA[2], boxA[3], boxB[2], boxB[3])
                if computeIoU(boxA, boxB) > iouThreshold or centerDistance < distanceThresholdRatio*maxDim:
                    unvisited.remove(other); stack.append(other); component.add(other)
        clusters.append([nonContained[i] for i in component])
    # 3) Merge each cluster into its bounding union
    merged: List[Tuple[int,int,int,int]] = []
    for cluster in clusters:
        xs = [r[0] for r in cluster]; ys = [r[1] for r in cluster]
        xEnds = [r[0]+r[2] for r in cluster]; yEnds = [r[1]+r[3] for r in cluster]
        xMin, yMin = min(xs), min(ys); xMax, yMax = max(xEnds), max(yEnds)
        merged.append((xMin, yMin, xMax-xMin, yMax-yMin))
    return merged