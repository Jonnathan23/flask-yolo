from app.utils.imageObjective import ImageObjective
        
#* Data P
class OperationDetector:
    LBP = "LBP"
    SIFT = "SIFT"

operation = OperationDetector.SIFT
pathImage = "app/static/img/astro.png"

imageObjective = ImageObjective(pathImage, objectId="selectImage")