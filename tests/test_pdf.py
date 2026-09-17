from pathlib import Path

import fitz
import pytest

from document_ocr.documents.pdf import PDFDocument
from document_ocr.documents.pdf_ocr import PDFOCR
from tests.fakes import FakeOCREngine


def create_pdf(path: Path, pages: int = 1) -> None:
    document = fitz.open()
    for page_number in range(pages):
        page = document.new_page()
        page.insert_text(
            (72, 72),
            f"Page {page_number + 1}",
        )

    document.save(path)
    document.close()


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
    file_path = tmp_path / "sample.pdf"
    create_pdf(file_path)
    with pytest.raises(ValueError):
        PDFDocument(
            file_path,
            dpi=0,
        )


def test_page_count(tmp_path):
    file_path = tmp_path / "sample.pdf"
    create_pdf(
        file_path,
        pages=3,
    )
    pdf = PDFDocument(file_path)
    assert pdf.page_count() == 3


def test_max_pages_validation():
    with pytest.raises(ValueError):
        PDFOCR(
            engine=None,
            max_pages=0,
        )


def test_invalid_dpi_pdf_ocr():
    with pytest.raises(ValueError):
        PDFOCR(
            engine=None,
            dpi=0,
        )


def test_pdf_ocr_max_pages(tmp_path):

    file_path = tmp_path / "sample.pdf"

    create_pdf(
        file_path,
        pages=5,
    )

    engine = FakeOCREngine()

    processor = PDFOCR(
        engine=engine,
        dpi=100,
        max_pages=2,
    )

    results = processor.process(
        file_path,
        language="eng",
    )

    assert len(results) == 2
    assert results[0].metadata["page"] == 1
    assert results[1].metadata["page"] == 2
    assert results[0].metadata["total_pages"] == 5


def test_pdf_ocr_progress(tmp_path):

    file_path = tmp_path / "sample.pdf"

    create_pdf(
        file_path,
        pages=3,
    )

    engine = FakeOCREngine()

    processor = PDFOCR(
        engine=engine,
        dpi=100,
    )

    progress = []

    def callback(
        current: int,
        total: int,
    ) -> None:

        progress.append((current, total))

    processor.process(
        file_path,
        progress_callback=callback,
    )

    assert progress == [
        (1, 3),
        (2, 3),
        (3, 3),
    ]
