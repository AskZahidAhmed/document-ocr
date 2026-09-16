from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image

from document_ocr.models.result import OCRResult


class OCREngine(ABC):
    @abstractmethod
    def extract_text(
        self,
        image: Path | Image.Image,
        language: str = "eng",
    ) -> OCRResult:
        """Extract text from an image."""
        raise NotImplementedError