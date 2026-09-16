from dataclasses import dataclass, field
from typing import Any


@dataclass
class OCRResult:
    text: str
    language: str
    confidence: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
