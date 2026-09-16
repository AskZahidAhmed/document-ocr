from abc import ABC, abstractmethod
from pathlib import Path

from document_ocr.models.result import OCRResult


class OCREngine(ABC):

    @abstractmethod
    def extract_text(
        self,
        image_path: Path,
        language: str = "eng",
    ) -> OCRResult:
        """Extract text from an image."""
        raise NotImplementedError
