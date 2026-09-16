from pathlib import Path

from PIL import Image, ImageFilter, ImageOps


class ImagePreprocessor:

    def __init__(
        self,
        grayscale: bool = True,
        denoise: bool = True,
        threshold: int | None = None,
        scale: float = 1.0,
    ):
        if scale <= 0:
            raise ValueError("scale must be greater than zero")

        if threshold is not None and not 0 <= threshold <= 255:
            raise ValueError(
                "threshold must be between 0 and 255"
            )

        self.grayscale = grayscale
        self.denoise = denoise
        self.threshold = threshold
        self.scale = scale

    def process(
        self,
        image: Path | Image.Image,
    ) -> Image.Image:

        if isinstance(image, Path):

            if not image.exists():
                raise FileNotFoundError(
                    f"Image file not found: {image}"
                )

            image = Image.open(image)

        elif not isinstance(image, Image.Image):

            raise TypeError(
                "image must be a Path or PIL.Image.Image"
            )

        image = ImageOps.exif_transpose(image)

        if self.grayscale:
            image = ImageOps.grayscale(image)

        if self.scale != 1.0:

            width, height = image.size

            image = image.resize(
                (
                    int(width * self.scale),
                    int(height * self.scale),
                )
            )

        if self.denoise:
            image = image.filter(
                ImageFilter.MedianFilter(size=3)
            )

        if self.threshold is not None:

            image = image.point(
                lambda pixel:
                255 if pixel >= self.threshold else 0
            )

        return image