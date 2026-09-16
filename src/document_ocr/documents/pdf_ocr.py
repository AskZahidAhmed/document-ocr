from pathlib import Path

from document_ocr.documents.pdf import PDFDocument
from document_ocr.engines.base import OCREngine
from document_ocr.models.result import OCRResult


class PDFOCR:
    def __init__(
        self,
        engine: OCREngine,
        dpi: int = 200,
    ):
        self.engine = engine
        self.dpi = dpi

    def process(
        self,
        pdf_path: Path,
        language: str = "eng",
    ) -> list[OCRResult]:

        pdf = PDFDocument(
            path=pdf_path,
            dpi=self.dpi,
        )

        results = []

        for page_number in range(
            1,
            pdf.page_count() + 1,
        ):
            image = pdf.render_page_as_image(page_number)

            result = self.engine.extract_text(
                image=image,
                language=language,
            )

            result.metadata.update(
                {
                    "document": str(pdf_path),
                    "page": page_number,
                    "dpi": self.dpi,
                }
            )

            results.append(result)

        return results
