from dataclasses import dataclass, field
from typing import Any

from document_ocr.models.page import OCRPage


@dataclass
class OCRDocument:
    source: str
    language: str
    pages: list[OCRPage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def text(self) -> str:
        return "\n\n".join(page.text for page in self.pages)

    @property
    def confidence(self) -> float | None:
        confidences = [
            page.confidence for page in self.pages if page.confidence is not None
        ]

        if not confidences:
            return None

        return sum(confidences) / len(confidences)
