from pathlib import Path

import pytesseract
from PIL import Image

from document_ocr.engines.base import OCREngine
from document_ocr.models.result import OCRResult


class TesseractEngine(OCREngine):

    def extract_text(
        self,
        image_path: Path,
        language: str = "eng",
    ) -> OCRResult:

        with Image.open(image_path) as image:
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