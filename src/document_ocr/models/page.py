from typing import Any
from dataclasses import dataclass, field
from document_ocr.models.result import OCRWord


@dataclass
class OCRPage:
    page_number: int
    text: str
    confidence: float | None = None
    words: list[OCRWord] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.page_number <= 0:
            raise ValueError("page_number must be greater than zero")
