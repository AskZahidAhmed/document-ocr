class DocumentOCRError(Exception):
    """Base exception for document OCR errors."""


class UnsupportedFileTypeError(DocumentOCRError):
    """Raised when a file type is not supported."""


class InvalidDocumentError(DocumentOCRError):
    """Raised when a document is invalid or unreadable."""


class FileSizeLimitError(DocumentOCRError):
    """Raised when a document exceeds the configured size limit."""
