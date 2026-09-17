from pathlib import Path

import fitz
from PIL import Image, UnidentifiedImageError

from document_ocr.exceptions import (
    FileSizeLimitError,
    InvalidDocumentError,
    UnsupportedFileTypeError,
)


class DocumentValidator:
    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tiff",
        ".tif",
        ".webp",
    }

    PDF_EXTENSIONS = {
        ".pdf"
    }

    def __init__(
        self,
        max_file_size_mb: float = 50,
    ):
        if max_file_size_mb <= 0:
            raise ValueError("max_file_size_mb must be greater than zero")

        self.max_file_size_bytes = int(max_file_size_mb * 1024 * 1024)

    def validate(self, path: Path) -> None:
        self.validate_exists(path)
        self.validate_file(path)
        self.validate_size(path)

        extension = path.suffix.lower()

        if extension in self.IMAGE_EXTENSIONS:
            self.validate_image(path)

        elif extension in self.PDF_EXTENSIONS:
            self.validate_pdf(path)

        else:
            raise UnsupportedFileTypeError(f"Unsupported file type: {extension}")

    def validate_exists(self, path: Path) -> None:
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

    def validate_file(self, path: Path) -> None:
        if not path.is_file():
            raise InvalidDocumentError(f"Expected a file: {path}")

    def validate_size(self, path: Path) -> None:
        file_size = path.stat().st_size

        if file_size > self.max_file_size_bytes:
            max_mb = self.max_file_size_bytes / (1024 * 1024)

            raise FileSizeLimitError(f"File exceeds maximum size of {max_mb:.1f} MB")

    def validate_image(self, path: Path) -> None:
        try:
            with Image.open(path) as image:
                image.verify()

        except (
            UnidentifiedImageError,
            OSError,
        ) as exc:
            raise InvalidDocumentError(f"Invalid image file: {path}") from exc

    def validate_pdf(self, path: Path) -> None:
        try:
            with fitz.open(path) as document:
                if document.page_count == 0:
                    raise InvalidDocumentError(f"PDF contains no pages: {path}")

        except (
            fitz.FileDataError,
            OSError,
        ) as exc:
            raise InvalidDocumentError(f"Invalid PDF file: {path}") from exc
