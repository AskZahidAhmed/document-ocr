from pathlib import Path

from document_ocr.documents.pdf_ocr import PDFOCR
from document_ocr.engines.tesseract import TesseractEngine
from document_ocr.preprocessing.image import ImagePreprocessor


def main() -> None:

    pdf_path = Path("examples/sample.pdf")

    preprocessor = ImagePreprocessor(
        grayscale=True,
        denoise=True,
        scale=1.0,
    )

    engine = TesseractEngine(
        preprocessor=preprocessor,
    )

    processor = PDFOCR(
        engine=engine,
        dpi=200,
    )

    results = processor.process(
        pdf_path=pdf_path,
        language="eng",
    )

    for result in results:

        print("=" * 60)

        print(
            f"Page: {result.metadata['page']}"
        )

        print(
            f"Confidence: {result.confidence}"
        )

        print()

        print(result.text)


if __name__ == "__main__":
    main()