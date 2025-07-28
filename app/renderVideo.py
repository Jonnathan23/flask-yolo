import cv2
import cv2 as cv
import time
import numpy as np

from app.data.db import  operation, imageObjective
from app.detectionObjects import executeDetection
from app.classes.index import OperationDetector
from app.utils.utils import drawSiftResults


def video_capture_local():
    """Genera un stream MJPEG desde la cámara local.

    Abre `cv2.VideoCapture(0)`, lee fotogramas, los convierte a gris
    y los emite codificados en JPEG para streaming HTTP.
    """
    print("Iniciando captura de video local...")
    width = 320
    height = 240
    fullWidth = width * 3
    
    prev_time = time.perf_counter() 
    cap = cv2.VideoCapture(0)
    
    canvas = np.zeros((height, fullWidth, 3), dtype=np.uint8) 
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara local")
    try:       
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (width, height)) 
            # panel izquierdo: imagen sin procesar
            canvas[:, :width] = frame
            
            result = executeDetection[operation](frame)
            
            # —————————————— Preprocesado ——————————————
            frame = cv.resize(frame, (width, height))
            now   = time.perf_counter()
            fps   = 1.0 / (now - prev_time) if now != prev_time else 0.0
            prev_time = now
            cv.putText(frame, f"FPS: {fps:.1f}",
                (10,30), cv.FONT_HERSHEY_SIMPLEX,
                1, (255,255,255), 2, cv.LINE_AA)

            # —————————————— Detección SIFT/LBP ——————————————
            result = executeDetection[operation](frame)

            # panel derecho: dibujo de keypoints o de matches
            if operation == OperationDetector.SIFT and result.found and result.goodMatches:
                drawSiftResults(result, frame, width, height, canvas)
            
            if operation == OperationDetector.LBP:
                # para LBP u otras operaciones
                canvas[:, width:width*2] = result           
            
            else:
                # panel derecho: imagen sin procesar
                canvas[:, width:width*2] = frame            
            _, encoded = cv2.imencode('.jpg', canvas)
            yield (b'--frame\r\n'                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
            
    finally:
        cap.release()
