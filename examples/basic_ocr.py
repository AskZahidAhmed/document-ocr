from pathlib import Path

from document_ocr.engines.tesseract import TesseractEngine
from document_ocr.preprocessing.image import ImagePreprocessor


def main() -> None:
    image_path = Path("examples/sample.png")
    preprocessor = ImagePreprocessor(grayscale=True, denoise=True, scale=2.0)
    engine = TesseractEngine(preprocessor=preprocessor)
    result = engine.extract_text(image_path=image_path, language="eng+hin")
    print("Engine:", result.metadata["engine"])
    print("Language:", result.language)
    print("Confidence:", result.confidence)
    print()
    print(result.text)


if __name__ == "__main__":
    main()