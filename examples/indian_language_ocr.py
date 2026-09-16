from pathlib import Path
from document_ocr.engines.tesseract import TesseractEngine
from document_ocr.preprocessing.image import ImagePreprocessor


def main() -> None:
    image_path = Path("examples/sample_hindi.png")

    preprocessor = ImagePreprocessor(
        grayscale=True,
        denoise=False,
        scale=2.0,
    )

    engine = TesseractEngine(
        preprocessor=preprocessor,
    )

    result = engine.extract_text(
        image_path,
        language="hin",
    )

    print("Engine:", result.metadata["engine"])
    print("Language:", result.language)
    print("Confidence:", result.confidence)
    print()
    print(result.text)


if __name__ == "__main__":
    main()
