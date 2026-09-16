from pathlib import Path

import pytest

from document_ocr.models.document import Document
from document_ocr.models.result import OCRResult
from document_ocr.preprocessing.image import ImagePreprocessor


def test_document_model():
    document = Document(
        path=Path("sample.png"),
        document_type="image",
    )

    assert document.path == Path("sample.png")
    assert document.document_type == "image"


def test_ocr_result():
    result = OCRResult(
        text="Hello",
        language="eng",
        confidence=95.0,
    )

    assert result.text == "Hello"
    assert result.language == "eng"
    assert result.confidence == 95.0


def test_invalid_scale():
    with pytest.raises(ValueError):
        ImagePreprocessor(scale=0)


def test_invalid_threshold():
    with pytest.raises(ValueError):
        ImagePreprocessor(threshold=300)