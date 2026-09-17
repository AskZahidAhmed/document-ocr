from collections.abc import Callable
from pathlib import Path

from document_ocr.documents.pdf import PDFDocument
from document_ocr.engines.base import OCREngine
from document_ocr.exceptions import InvalidDocumentError
from document_ocr.models.ocr_document import OCRDocument
from document_ocr.models.page import OCRPage
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
    ) -> OCRDocument:

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

        pages: list[OCRPage] = []

        for page_number in range(
            1,
            pages_to_process + 1,
        ):
            try:
                image = pdf.render_page_as_image(page_number)

                result = self.engine.extract_text(
                    image=image,
                    language=language,
                )

                page = OCRPage(
                    page_number=page_number,
                    text=result.text,
                    confidence=result.confidence,
                    words=result.words,
                    metadata={
                        "dpi": self.dpi,
                        "engine": result.metadata.get("engine"),
                    },
                )

                pages.append(page)

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

        return OCRDocument(
            source=str(pdf_path),
            language=language,
            pages=pages,
            metadata={
                "document_type": "pdf",
                "total_pages": total_pages,
                "processed_pages": len(pages),
                "dpi": self.dpi,
                "engine": self.engine.name(),
            },
        )
