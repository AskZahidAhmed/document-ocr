from pathlib import Path

import pytest

from document_ocr.models.document import Document
from document_ocr.models.result import OCRResult, OCRWord
from document_ocr.preprocessing.image import ImagePreprocessor


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