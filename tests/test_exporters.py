import json

from document_ocr.exporters.json import JSONExporter
from document_ocr.exporters.text import TextExporter
from document_ocr.models.result import OCRResult, OCRWord


def create_result() -> OCRResult:
    return OCRResult(
        text="Hello भारत",
        language="hin+eng",
        confidence=95.5,
        words=[
            OCRWord(
                text="Hello",
                confidence=96.0,
                x=10,
                y=20,
                width=50,
                height=25,
            ),
            OCRWord(
                text="भारत",
                confidence=95.0,
                x=70,
                y=20,
                width=60,
                height=25,
            ),
        ],
        metadata={
            "engine": "tesseract",
            "page": 1,
        },
    )


def test_json_export(tmp_path):

    output_path = tmp_path / "result.json"

    result = create_result()

    exporter = JSONExporter()

    exporter.export(
        result,
        output_path,
    )

    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))

    assert data["text"] == "Hello भारत"
    assert data["language"] == "hin+eng"
    assert data["confidence"] == 95.5

    assert len(data["words"]) == 2

    assert data["words"][0]["text"] == "Hello"
    assert data["words"][1]["text"] == "भारत"


def test_text_export(tmp_path):

    output_path = tmp_path / "result.txt"

    result = create_result()

    exporter = TextExporter()

    exporter.export(
        result,
        output_path,
    )

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert content == "Hello भारत"
