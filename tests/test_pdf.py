from pathlib import Path

import pytest

from document_ocr.documents.pdf import PDFDocument


def test_missing_pdf():
    with pytest.raises(FileNotFoundError):
        PDFDocument(Path("missing.pdf"))


def test_invalid_extension(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "test",
        encoding="utf-8",
    )

    with pytest.raises(ValueError):
        PDFDocument(file_path)


def test_invalid_dpi(tmp_path):
    file_path = Path("examples/sample.png")
    # file_path = tmp_path / "sample.pdf"
    with pytest.raises(ValueError):
        PDFDocument(file_path, dpi=0)
