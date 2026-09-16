from pathlib import Path

from document_ocr.engines.tesseract import TesseractEngine
from document_ocr.exporters.json import JSONExporter
from document_ocr.exporters.text import TextExporter
from document_ocr.preprocessing.image import ImagePreprocessor


def main() -> None:

    image_path = Path("examples/sample.png")

    json_output = Path("output/result.json")
    text_output = Path("output/result.txt")

    preprocessor = ImagePreprocessor(
        grayscale=True,
        denoise=True,
        scale=2.0,
    )

    engine = TesseractEngine(
        preprocessor=preprocessor,
    )

    result = engine.extract_text(
        image_path,
        language="eng+hin",
    )

    JSONExporter().export(
        result,
        json_output,
    )

    TextExporter().export(
        result,
        text_output,
    )

    print("OCR completed")
    print()
    print("Text:", text_output)
    print("JSON:", json_output)
    print()
    print("Confidence:", result.confidence)
    print("Words:", len(result.words))


if __name__ == "__main__":
    main()
