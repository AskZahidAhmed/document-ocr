from pathlib import Path

from document_ocr.documents.pdf_ocr import PDFOCR
from document_ocr.engines.tesseract import TesseractEngine
from document_ocr.preprocessing.image import ImagePreprocessor


def show_progress(
    current: int,
    total: int,
) -> None:

    percentage = (current / total) * 100

    print(f"Progress: {current}/{total} ({percentage:.1f}%)")


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
        max_pages=20,
        stop_on_error=True,
    )

    results = processor.process(
        pdf_path=pdf_path,
        language="eng",
        progress_callback=show_progress,
    )

    for result in results:
        print("=" * 60)

        print(f"Page: {result.metadata['page']}")

        print(f"Confidence: {result.confidence}")

        print()

        print(result.text)


if __name__ == "__main__":
    main()
