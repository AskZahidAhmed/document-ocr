from dataclasses import dataclass, field
from typing import Any


@dataclass
class OCRWord:
    text: str
    confidence: float
    x: int
    y: int
    width: int
    height: int


@dataclass
class OCRResult:
    text: str
    language: str
    confidence: float | None = None
    words: list[OCRWord] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)