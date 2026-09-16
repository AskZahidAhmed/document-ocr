from abc import ABC, abstractmethod
from pathlib import Path

from document_ocr.models.result import OCRResult


class OCRExporter(ABC):
    @abstractmethod
    def export(
        self,
        result: OCRResult,
        output_path: Path,
    ) -> None:
        """Export OCR result to a file."""
        raise NotImplementedError
