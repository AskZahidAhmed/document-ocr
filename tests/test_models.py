from pathlib import Path

import pytest

from document_ocr.models.document import Document
from document_ocr.models.result import OCRResult, OCRWord
from document_ocr.preprocessing.image import ImagePreprocessor

from document_ocr.models.ocr_document import OCRDocument
from document_ocr.models.page import OCRPage


def test_document_model():
    document = Document(
        path=Path("sample.png"),
        document_type="image",
    )

    assert document.path == Path("sample.png")
    assert document.document_type == "image"


def test_ocr_word():
    word = OCRWord(
        text="Hello",
        confidence=95.5,
        x=100,
        y=50,
        width=80,
        height=30,
    )

    assert word.text == "Hello"
    assert word.confidence == 95.5
    assert word.x == 100
    assert word.y == 50
    assert word.width == 80
    assert word.height == 30


def test_ocr_result():
    word = OCRWord(
        text="Hello",
        confidence=95.0,
        x=10,
        y=20,
        width=50,
        height=20,
    )

    result = OCRResult(
        text="Hello",
        language="eng",
        confidence=95.0,
        words=[word],
    )

    assert result.text == "Hello"
    assert result.language == "eng"
    assert result.confidence == 95.0
    assert len(result.words) == 1
    assert result.words[0].text == "Hello"


def test_invalid_scale():
    with pytest.raises(ValueError):
        ImagePreprocessor(scale=0)


def test_invalid_threshold():
    with pytest.raises(ValueError):
        ImagePreprocessor(threshold=300)


def test_ocr_page():

    page = OCRPage(
        page_number=1,
        text="Hello भारत",
        confidence=95.0,
    )

    assert page.page_number == 1
    assert page.text == "Hello भारत"
    assert page.confidence == 95.0


def test_invalid_page_number():

    with pytest.raises(ValueError):
        OCRPage(
            page_number=0,
            text="Hello",
        )


def test_ocr_document():

    page1 = OCRPage(
        page_number=1,
        text="Hello",
        confidence=90.0,
    )

    page2 = OCRPage(
        page_number=2,
        text="World",
        confidence=100.0,
    )

    document = OCRDocument(
        source="sample.pdf",
        language="eng",
        pages=[
            page1,
            page2,
        ],
    )

    assert document.page_count == 2
    assert document.text == "Hello\n\nWorld"
    assert document.confidence == 95.0
