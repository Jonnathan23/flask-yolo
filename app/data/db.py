from app.classes.index import ImageObjective, OperationDetector
        
#* Data P

operation = OperationDetector.SIFT
pathImage = "app/static/img/astro.png"

imageObjective = ImageObjective(pathImage, objectId="selectImage")