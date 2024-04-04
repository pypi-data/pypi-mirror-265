from PIL import Image


class ImageTransform:
    def __call__(self, image: Image.Image) -> Image.Image:
        return image