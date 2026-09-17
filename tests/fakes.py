from pathlib import Path

from PIL import Image

from document_ocr.engines.base import OCREngine
from document_ocr.models.result import OCRResult


class FakeOCREngine(OCREngine):
    def name(self) -> str:
        return "fake"

    def supported_languages(self) -> list[str]:
        return ["eng"]

    def extract_text(
        self,
        image: Path | Image.Image,
        language: str = "eng",
    ) -> OCRResult:

        return OCRResult(
            text="fake OCR result",
            language=language,
            confidence=100.0,
            metadata={
                "engine": self.name(),
            },
        )
