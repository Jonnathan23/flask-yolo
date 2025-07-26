from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Tuple
from numpy.typing import NDArray
import numpy as np
import cv2 as cv


@dataclass
class ImageObjective:
    """Representa una imagen de referencia + sus datos SIFT precalculados."""
    image: NDArray[np.uint8]
    keyPoints: List[cv.KeyPoint]
    descriptors: NDArray[np.float32]
    objectId: Optional[str] = None

    # --- CONSTRUCTOR “todo en uno” ---------------------------------
    def __init__(
        self,
        filePath: str,
        objectId: str | None = None,
        siftParams: Tuple[int, int, float, float] = (800, 3, 0.06, 10),
        applyRootSift: bool = True,
    ):
        print(f"Inicializando ImageObjective con '{filePath}'")
        self.objectId = objectId

        # 1. Leer la imagen en BGR uint8
        self.image: NDArray[np.uint8] = cv.imread(filePath)
        if self.image is None:
            raise FileNotFoundError(f"No se pudo abrir '{filePath}'")

        # 2. Preparar detector SIFT con los parámetros deseados
        nFeatures, nLayers, contrastTh, edgeTh = siftParams
        sift: cv.SIFT = cv.SIFT_create(
            nfeatures=nFeatures,
            nOctaveLayers=nLayers,
            contrastThreshold=contrastTh,
            edgeThreshold=edgeTh,
        )

        # 3. Detectar y describir
        self.keyPoints, self.descriptors = sift.detectAndCompute(self.image, None)

        # 4. RootSIFT (opcional)
        if applyRootSift and self.descriptors is not None:
            cv.normalize(self.descriptors, self.descriptors, 1, 0, cv.NORM_L1)
            cv.sqrt(self.descriptors, self.descriptors)
            
        if self.descriptors is None or self.descriptors.shape[0] < 2:
            raise ValueError(
                f"La imagen '{filePath}' produjo menos de dos descriptores SIFT. "
                "Prueba con una versión de mayor resolución o más contraste."
            )

    # --------- ayuditas opcionales ---------------------------------
    @property
    def shape(self) -> tuple[int, int, int]:
        return self.image.shape

    def __repr__(self) -> str:
        return (
            f"ImageObjective(id={self.objectId}, "
            f"kp={len(self.keyPoints)}, shape={self.shape})"
        )