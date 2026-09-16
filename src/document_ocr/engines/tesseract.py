from pathlib import Path

import pytesseract
from PIL import Image

from document_ocr.engines.base import OCREngine
from document_ocr.models.result import OCRResult, OCRWord
from document_ocr.preprocessing.image import ImagePreprocessor


class TesseractEngine(OCREngine):

    def __init__(
        self,
        preprocessor: ImagePreprocessor | None = None,
    ):
        self.preprocessor = preprocessor

    def _load_image(
        self,
        image: Path | Image.Image,
    ) -> Image.Image:

        if isinstance(image, Path):

            if not image.exists():
                raise FileNotFoundError(
                    f"Image file not found: {image}"
                )

            with Image.open(image) as opened_image:
                return opened_image.copy()

        if isinstance(image, Image.Image):
            return image.copy()

        raise TypeError(
            "image must be a Path or PIL.Image.Image"
        )

    def extract_text(
        self,
        image: Path | Image.Image,
        language: str = "eng",
    ) -> OCRResult:

        image = self._load_image(image)

        if self.preprocessor:
            image = self.preprocessor.process(image)

        text = pytesseract.image_to_string(
            image,
            lang=language,
        )

        data = pytesseract.image_to_data(
            image,
            lang=language,
            output_type=pytesseract.Output.DICT,
        )

        words: list[OCRWord] = []
        confidences: list[float] = []

        for index, raw_text in enumerate(data["text"]):

            word = raw_text.strip()

            if not word:
                continue

            raw_confidence = data["conf"][index]

            try:
                confidence = float(raw_confidence)
            except (TypeError, ValueError):
                continue

            if confidence < 0:
                continue

            words.append(
                OCRWord(
                    text=word,
                    confidence=confidence,
                    x=int(data["left"][index]),
                    y=int(data["top"][index]),
                    width=int(data["width"][index]),
                    height=int(data["height"][index]),
                )
            )

            confidences.append(confidence)

        overall_confidence = (
            sum(confidences) / len(confidences)
            if confidences
            else None
        )

        return OCRResult(
            text=text.strip(),
            language=language,
            confidence=overall_confidence,
            words=words,
            metadata={
                "engine": "tesseract",
            },
        )