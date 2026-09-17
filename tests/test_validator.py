from pathlib import Path

import pytest
from PIL import Image

from document_ocr.exceptions import (
    FileSizeLimitError,
    InvalidDocumentError,
    UnsupportedFileTypeError,
)
from document_ocr.validators.document import DocumentValidator


def test_missing_file():

    validator = DocumentValidator()

    with pytest.raises(FileNotFoundError):
        validator.validate(Path("missing.png"))


def test_unsupported_file(tmp_path):

    file_path = tmp_path / "sample.txt"

    file_path.write_text(
        "hello",
        encoding="utf-8",
    )

    validator = DocumentValidator()

    with pytest.raises(UnsupportedFileTypeError):
        validator.validate(file_path)


def test_valid_image(tmp_path):

    file_path = tmp_path / "sample.png"

    image = Image.new(
        "RGB",
        (100, 100),
        "white",
    )

    image.save(file_path)

    validator = DocumentValidator()

    validator.validate(file_path)


def test_invalid_image(tmp_path):

    file_path = tmp_path / "invalid.png"

    file_path.write_text(
        "not an image",
        encoding="utf-8",
    )

    validator = DocumentValidator()

    with pytest.raises(InvalidDocumentError):
        validator.validate(file_path)


def test_file_size_limit(tmp_path):

    file_path = tmp_path / "large.png"

    file_path.write_bytes(b"x" * 1024)

    validator = DocumentValidator(max_file_size_mb=0.0001)

    with pytest.raises(FileSizeLimitError):
        validator.validate(file_path)
