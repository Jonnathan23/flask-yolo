import cv2
from app.data.db import  operation
from app.detectionObjects import executeDetection

def video_capture_local():
    """Genera un stream MJPEG desde la cámara local.

    Abre `cv2.VideoCapture(0)`, lee fotogramas, los convierte a gris
    y los emite codificados en JPEG para streaming HTTP.
    """
    print("Iniciando captura de video local...")
    
    cap = cv2.VideoCapture(0)    
    if not cap.isOpened():
        raise RuntimeError("No se pudo abrir la cámara local")
    try:       
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            result = executeDetection[operation](frame)
            
            _, encoded = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'                   b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
            
    finally:
        cap.release()
