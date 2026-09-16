from pathlib import Path
from document_ocr.engines.tesseract import TesseractEngine


def main() -> None:
    image_path = Path("examples/sample.png")
    engine = TesseractEngine()
    result = engine.extract_text(image_path=image_path, language="eng+hin")
    print("Language:", result.language)
    print("Confidence:", result.confidence)
    print()
    print(result.text)


if __name__ == "__main__":
    main()
