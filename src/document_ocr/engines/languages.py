from dataclasses import dataclass


@dataclass(frozen=True)
class OCRLanguage:
    code: str
    name: str
    native_name: str


SUPPORTED_LANGUAGES = {
    "eng": OCRLanguage(
        code="eng",
        name="English",
        native_name="English",
    ),
    "hin": OCRLanguage(
        code="hin",
        name="Hindi",
        native_name="हिन्दी",
    ),
    "ben": OCRLanguage(
        code="ben",
        name="Bengali",
        native_name="বাংলা",
    ),
    "guj": OCRLanguage(
        code="guj",
        name="Gujarati",
        native_name="ગુજરાતી",
    ),
    "kan": OCRLanguage(
        code="kan",
        name="Kannada",
        native_name="ಕನ್ನಡ",
    ),
    "mal": OCRLanguage(
        code="mal",
        name="Malayalam",
        native_name="മലയാളം",
    ),
    "mar": OCRLanguage(
        code="mar",
        name="Marathi",
        native_name="मराठी",
    ),
    "ori": OCRLanguage(
        code="ori",
        name="Odia",
        native_name="ଓଡ଼ିଆ",
    ),
    "pan": OCRLanguage(
        code="pan",
        name="Punjabi",
        native_name="ਪੰਜਾਬੀ",
    ),
    "tam": OCRLanguage(
        code="tam",
        name="Tamil",
        native_name="தமிழ்",
    ),
    "tel": OCRLanguage(
        code="tel",
        name="Telugu",
        native_name="తెలుగు",
    ),
    "urd": OCRLanguage(
        code="urd",
        name="Urdu",
        native_name="اردو",
    ),
}


def get_language(
    code: str,
) -> OCRLanguage:

    try:
        return SUPPORTED_LANGUAGES[code]
    except KeyError as exc:
        raise ValueError(f"Unknown OCR language: {code}") from exc


def get_language_codes() -> list[str]:
    return list(SUPPORTED_LANGUAGES)
