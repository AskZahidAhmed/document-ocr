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

    def name(self) -> str:
        return "tesseract"

    def supported_languages(self) -> list[str]:
        return pytesseract.get_languages(config="")

    def _validate_language(
        self,
        language: str,
    ) -> None:

        supported = self.supported_languages()

        requested_languages = language.split("+")

        unsupported = [lang for lang in requested_languages if lang not in supported]

        if unsupported:
            raise ValueError("Unsupported OCR language(s): " + ", ".join(unsupported))

    def _load_image(
        self,
        image: Path | Image.Image,
    ) -> Image.Image:

        if isinstance(image, Path):
            if not image.exists():
                raise FileNotFoundError(f"Image file not found: {image}")

            with Image.open(image) as opened_image:
                return opened_image.copy()

        if isinstance(image, Image.Image):
            return image.copy()

        raise TypeError("image must be a Path or PIL.Image.Image")

    def extract_text(
        self,
        image: Path | Image.Image,
        language: str = "eng",
    ) -> OCRResult:

        self._validate_language(language)

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

            try:
                confidence = float(data["conf"][index])
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
            sum(confidences) / len(confidences) if confidences else None
        )

        return OCRResult(
            text=text.strip(),
            language=language,
            confidence=overall_confidence,
            words=words,
            metadata={
                "engine": self.name(),
            },
        )
