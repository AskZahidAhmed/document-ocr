import pytest

from document_ocr.engines.languages import (
    SUPPORTED_LANGUAGES,
    get_language,
    get_language_codes,
)


def test_hindi_language():

    language = get_language("hin")

    assert language.code == "hin"
    assert language.name == "Hindi"
    assert language.native_name == "हिन्दी"


def test_english_language():

    language = get_language("eng")

    assert language.code == "eng"
    assert language.name == "English"


def test_supported_language_codes():

    codes = get_language_codes()

    assert "eng" in codes
    assert "hin" in codes
    assert "tam" in codes
    assert "tel" in codes


def test_unknown_language():

    with pytest.raises(ValueError):
        get_language("xyz")
