from pathlib import Path

from document_ocr.exporters.base import OCRExporter
from document_ocr.models.ocr_document import OCRDocument
from document_ocr.models.result import OCRResult


class TextExporter(OCRExporter):
    def export(
        self,
        result: OCRResult | OCRDocument,
        output_path: Path,
    ) -> None:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            result.text,
            encoding="utf-8",
        )
