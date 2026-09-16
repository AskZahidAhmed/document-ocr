from io import BytesIO
from pathlib import Path

import fitz
from PIL import Image


class PDFDocument:

    def __init__(self, path: Path, dpi: int = 200):
        if not path.exists():
            raise FileNotFoundError(
                f"PDF file not found: {path}"
            )

        if path.suffix.lower() != ".pdf":
            raise ValueError(
                f"Expected PDF file, got: {path.suffix}"
            )

        if dpi <= 0:
            raise ValueError("dpi must be greater than zero")

        self.path = path
        self.dpi = dpi

    def page_count(self) -> int:

        with fitz.open(self.path) as document:
            return len(document)

    def render_page(self, page_number: int):

        with fitz.open(self.path) as document:

            if page_number < 1 or page_number > len(document):
                raise ValueError(
                    f"Invalid page number: {page_number}"
                )

            page = document[page_number - 1]

            scale = self.dpi / 72

            matrix = fitz.Matrix(scale, scale)

            return page.get_pixmap(
                matrix=matrix,
                alpha=False,
            )

    def render_page_as_image(
        self,
        page_number: int,
    ) -> Image.Image:

        pixmap = self.render_page(page_number)

        image_bytes = pixmap.tobytes("png")

        return Image.open(
            BytesIO(image_bytes)
        )