import json
from dataclasses import asdict
from pathlib import Path

from document_ocr.exporters.base import OCRExporter
from document_ocr.models.result import OCRResult


class JSONExporter(OCRExporter):
    def export(
        self,
        result: OCRResult,
        output_path: Path,
    ) -> None:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            json.dumps(
                asdict(result),
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
