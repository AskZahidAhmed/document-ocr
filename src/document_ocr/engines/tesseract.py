from pathlib import Path

import pytesseract

from document_ocr.engines.base import OCREngine
from document_ocr.models.result import OCRResult
from document_ocr.preprocessing.image import ImagePreprocessor


class TesseractEngine(OCREngine):

    def __init__(
        self,
        preprocessor: ImagePreprocessor | None = None,
    ):
        self.preprocessor = preprocessor

    def extract_text(
        self,
        image_path: Path,
        language: str = "eng",
    ) -> OCRResult:

        if self.preprocessor:
            image = self.preprocessor.process(image_path)
        else:
            from PIL import Image

            image = Image.open(image_path)

        text = pytesseract.image_to_string(
            image,
            lang=language,
        )

        data = pytesseract.image_to_data(
            image,
            lang=language,
            output_type=pytesseract.Output.DICT,
        )

        confidences = [
            float(value)
            for value in data["conf"]
            if str(value).strip() not in {"", "-1"}
        ]

        confidence = (
            sum(confidences) / len(confidences)
            if confidences
            else None
        )

        return OCRResult(
            text=text.strip(),
            language=language,
            confidence=confidence,
            metadata={
                "engine": "tesseract",
                "source": str(image_path),
            },
        )