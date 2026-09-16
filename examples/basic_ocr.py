from pathlib import Path

from document_ocr.engines.tesseract import TesseractEngine
from document_ocr.preprocessing.image import ImagePreprocessor


def main() -> None:
    image_path = Path("examples/sample.png")

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
        language="eng",
    )

    print("Engine:", result.metadata["engine"])
    print("Language:", result.language)
    print("Confidence:", result.confidence)
    print()

    print("TEXT")
    print("-" * 60)
    print(result.text)
    print()

    print("WORDS")
    print("-" * 60)

    for word in result.words:
        print(
            f"text={word.text!r}, "
            f"confidence={word.confidence:.2f}, "
            f"x={word.x}, "
            f"y={word.y}, "
            f"width={word.width}, "
            f"height={word.height}"
        )


if __name__ == "__main__":
    main()