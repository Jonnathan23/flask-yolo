import cv2
from app.classes.index import ImageObjective, OperationDetector
        
#* Data P

operation = OperationDetector.LBP
pathImage = "app/static/img/astro.png"
pathLBP = "app/static/model/cascade.xml"

imageObjective = ImageObjective(pathImage, objectId="selectImage")

detector = cv2.CascadeClassifier(pathLBP)
if detector.empty():
    print(f"❌ No se pudo cargar el clasificador desde: {pathLBP}")   