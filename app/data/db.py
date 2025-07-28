import cv2
from app.classes.index import ImageObjective, OperationDetector
        
#* Data P
print( "Inicializando base de datos...")
operation = ""
pathImage = "app/static/img/astro.png"
pathLBP = "app/static/model/cascade.xml"

ipMobile = "0"
imageObjective = ImageObjective(pathImage, objectId="selectImage")

detector = cv2.CascadeClassifier(pathLBP)
if detector.empty():
    print(f"❌ No se pudo cargar el clasificador desde: {pathLBP}")   