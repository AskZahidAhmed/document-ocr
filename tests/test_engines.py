import pytest

from document_ocr.engines.tesseract import TesseractEngine


def test_tesseract_engine_name():

    engine = TesseractEngine()

    assert engine.name() == "tesseract"


def test_tesseract_supported_languages():

    engine = TesseractEngine()

    languages = engine.supported_languages()

    assert isinstance(languages, list)
    assert "eng" in languages


def test_unsupported_language():

    engine = TesseractEngine()

    with pytest.raises(ValueError):
        engine.extract_text(
            image=None,
            language="xyz",
        )


def test_hindi_english_language_validation():

    engine = TesseractEngine()

    languages = engine.supported_languages()

    if not {
        "hin",
        "eng",
    }.issubset(languages):
        pytest.skip("Hindi and English language packs are not installed")

    engine._validate_language("hin+eng")
