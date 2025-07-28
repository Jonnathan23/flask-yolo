import cv2
import cv2 as cv
import time
import numpy as np
import socket

import app.data.db as db
from app.detectionObjects import executeDetection
from app.classes.index import OperationDetector
from app.utils.utils import drawSiftResults


def video_capture_local():
    """Genera un stream MJPEG desde la cámara local.   """
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
            
            result = executeDetection[db.operation](frame)
            
            # —————————————— Preprocesado ——————————————
            frame = cv.resize(frame, (width, height))
            now   = time.perf_counter()
            fps   = 1.0 / (now - prev_time) if now != prev_time else 0.0
            prev_time = now
            cv.putText(frame, f"FPS: {fps:.1f}",
                (10,30), cv.FONT_HERSHEY_SIMPLEX,
                1, (255,255,255), 2, cv.LINE_AA)            

            # panel derecho: dibujo de keypoints o de matches
            if db.operation == OperationDetector.SIFT and result.found and result.goodMatches:
                drawSiftResults(result, frame, width, height, canvas)
            
            if db.operation == OperationDetector.LBP:
                # para LBP u otras operaciones
                canvas[:, width:width*2] = result           
            
            else:
                # panel derecho: imagen sin procesar
                canvas[:, width:width*2] = frame            
            _, encoded = cv2.imencode('.jpg', canvas)
            yield (b'--frame\r\n'                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
            
    finally:
        cap.release()


def video_capture_mobile():
    # Crea y enlaza el socket UDP al puerto donde la app envía los datagramas
    print("Iniciando captura de video móvil...")
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(("0.0.0.0", 5005))

    prevTime = time.perf_counter()
    
    width = 320
    height = 240
    fullWidth = width * 3
    
    width, height, fullWidth = 320, 240, 320*3
    canvas = np.zeros((height, fullWidth, 3), dtype=np.uint8)
    prevTime = time.perf_counter()

    while True:
        frameBytes, _ = serverSocket.recvfrom(65536)
        npArray = np.frombuffer(frameBytes, dtype=np.uint8)
        frame = cv2.imdecode(npArray, cv2.IMREAD_COLOR)
        if frame is None: continue  # conditional en una sola línea

        # redimensionar y dibujar original
        frameResized = cv2.resize(frame, (width, height))
        canvas[:, :width] = frameResized

        # detección según operación
        result = executeDetection[db.operation](frameResized)

        # cálculo de FPS
        now = time.perf_counter()
        fps = 1.0/(now-prevTime) if now!=prevTime else 0.0
        prevTime = now
        cv2.putText(frameResized,
                    f"FPS: {fps:.1f}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2,
                    cv2.LINE_AA)

        # panel derecho: SIFT / LBP / original
        if db.operation==OperationDetector.SIFT and result.found and result.goodMatches:
            drawSiftResults(result, frameResized, width, height, canvas)
        elif db.operation==OperationDetector.LBP:
            canvas[:, width:width*2] = result
        else:
            canvas[:, width:width*2] = frameResized

        # codificar y enviar
        success, encoded = cv2.imencode('.jpg', canvas)
        if not success: continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encoded) +
            b'\r\n'
        )
        
