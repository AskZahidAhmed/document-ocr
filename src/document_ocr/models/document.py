from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Document:
    path: Path
    document_type: str
    metadata: dict[str, Any] = field(default_factory=dict)