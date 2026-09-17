from collections.abc import Callable
from pathlib import Path

from document_ocr.documents.pdf import PDFDocument
from document_ocr.engines.base import OCREngine
from document_ocr.exceptions import InvalidDocumentError
from document_ocr.models.result import OCRResult
from document_ocr.validators.document import DocumentValidator


ProgressCallback = Callable[[int, int], None]


class PDFOCR:
    def __init__(
        self,
        engine: OCREngine,
        dpi: int = 200,
        validator: DocumentValidator | None = None,
        max_pages: int | None = None,
        stop_on_error: bool = True,
    ):
        if dpi <= 0:
            raise ValueError("dpi must be greater than zero")

        if max_pages is not None and max_pages <= 0:
            raise ValueError("max_pages must be greater than zero")

        self.engine = engine
        self.dpi = dpi
        self.validator = validator
        self.max_pages = max_pages
        self.stop_on_error = stop_on_error

    def process(
        self,
        pdf_path: Path,
        language: str = "eng",
        progress_callback: ProgressCallback | None = None,
    ) -> list[OCRResult]:

        if self.validator:
            self.validator.validate(pdf_path)

        pdf = PDFDocument(
            path=pdf_path,
            dpi=self.dpi,
        )

        total_pages = pdf.page_count()

        pages_to_process = total_pages

        if self.max_pages is not None:
            pages_to_process = min(
                total_pages,
                self.max_pages,
            )

        results: list[OCRResult] = []

        for page_number in range(1, pages_to_process + 1):
            try:
                image = pdf.render_page_as_image(page_number)
                result = self.engine.extract_text(image=image, language=language)
                result.metadata.update(
                    {
                        "document": str(pdf_path),
                        "page": page_number,
                        "total_pages": total_pages,
                        "dpi": self.dpi,
                    }
                )

                results.append(result)

            except Exception as exc:
                if self.stop_on_error:
                    raise InvalidDocumentError(
                        f"Failed to process PDF page {page_number}: {exc}"
                    ) from exc

            if progress_callback:
                progress_callback(
                    page_number,
                    pages_to_process,
                )

        return results
