import io
from base64 import b64decode, b64encode

from PIL import Image

from app.schemas import ImageResult


def image_to_bytes(image_data: Image.Image) -> bytes:
    img_byte_arr = io.BytesIO()
    image_data.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr.getvalue()


def bytes_to_image(img_byte_arr: bytes) -> Image.Image:
    image_data = io.BytesIO(img_byte_arr)
    return Image.open(image_data)


def encode_image(image_data: Image.Image) -> bytes:
    return b64encode(image_to_bytes(image_data))


def decode_image(img_byte_arr: bytes) -> Image.Image:
    return bytes_to_image(b64decode(img_byte_arr))


def resize_image(image: Image.Image) -> ImageResult:
    image32 = image.resize((32, 32))
    image64 = image.resize((64, 64))
    return ImageResult(
        IMAGE_32=encode_image(image32),
        IMAGE_64=encode_image(image64),
        IMAGE_ORIGINAL=encode_image(image),
    )
