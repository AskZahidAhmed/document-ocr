import argparse
from pathlib import Path

from document_ocr.documents.pdf_ocr import PDFOCR
from document_ocr.engines.tesseract import TesseractEngine
from document_ocr.exporters.json import JSONExporter
from document_ocr.exporters.text import TextExporter
from document_ocr.preprocessing.image import ImagePreprocessor
from document_ocr.validators.document import DocumentValidator


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="document-ocr",
        description=("Open-source OCR pipeline for images and scanned PDFs."),
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input image or PDF file.",
    )

    parser.add_argument(
        "--language",
        default="eng",
        help="OCR language, e.g. eng or hin+eng.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Output directory.",
    )

    parser.add_argument(
        "--format",
        choices=["json", "txt", "both"],
        default="both",
        help="Output format.",
    )

    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="PDF rendering DPI.",
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Maximum PDF pages to process.",
    )

    parser.add_argument(
        "--no-preprocess",
        action="store_true",
        help="Disable image preprocessing.",
    )

    parser.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Image preprocessing scale.",
    )

    parser.add_argument(
        "--threshold",
        type=int,
        default=None,
        help="Optional grayscale threshold (0-255).",
    )

    return parser


def create_engine(
    args: argparse.Namespace,
) -> TesseractEngine:

    preprocessor = None

    if not args.no_preprocess:
        preprocessor = ImagePreprocessor(
            grayscale=True,
            denoise=True,
            scale=args.scale,
            threshold=args.threshold,
        )

    return TesseractEngine(
        preprocessor=preprocessor,
    )


def show_progress(
    current: int,
    total: int,
) -> None:

    percentage = (current / total) * 100

    print(f"Processing page {current}/{total} ({percentage:.1f}%)")


def process_image(
    input_path: Path,
    output_dir: Path,
    engine: TesseractEngine,
    language: str,
    output_format: str,
) -> None:

    result = engine.extract_text(
        input_path,
        language=language,
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    stem = input_path.stem

    if output_format in {"json", "both"}:
        JSONExporter().export(
            result,
            output_dir / f"{stem}.json",
        )

    if output_format in {"txt", "both"}:
        TextExporter().export(
            result,
            output_dir / f"{stem}.txt",
        )

    print(f"OCR completed: {input_path}")

    print(f"Confidence: {result.confidence}")


def process_pdf(
    input_path: Path,
    output_dir: Path,
    engine: TesseractEngine,
    language: str,
    output_format: str,
    dpi: int,
    max_pages: int | None,
) -> None:

    processor = PDFOCR(
        engine=engine,
        dpi=dpi,
        max_pages=max_pages,
    )

    document = processor.process(
        input_path,
        language=language,
        progress_callback=show_progress,
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    stem = input_path.stem

    if output_format in {"json", "both"}:
        JSONExporter().export(
            document,
            output_dir / f"{stem}.json",
        )

    if output_format in {"txt", "both"}:
        TextExporter().export(
            document,
            output_dir / f"{stem}.txt",
        )

    print()
    print(f"OCR completed: {input_path}")

    print(f"Pages processed: {document.page_count}")

    print(f"Confidence: {document.confidence}")


def main() -> None:

    parser = create_parser()

    args = parser.parse_args()

    validator = DocumentValidator()

    try:
        validator.validate(args.input)

        engine = create_engine(args)

        extension = args.input.suffix.lower()

        if extension == ".pdf":
            process_pdf(
                input_path=args.input,
                output_dir=args.output,
                engine=engine,
                language=args.language,
                output_format=args.format,
                dpi=args.dpi,
                max_pages=args.max_pages,
            )

        else:
            process_image(
                input_path=args.input,
                output_dir=args.output,
                engine=engine,
                language=args.language,
                output_format=args.format,
            )

    except Exception as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
