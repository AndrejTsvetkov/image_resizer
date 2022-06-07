from app.image_process import resize_image


def test_resize_image(image, image_32_base64, image_64_base64, image_base64):
    result = resize_image(image)
    assert result.IMAGE_32 == image_32_base64
    assert result.IMAGE_64 == image_64_base64
    assert result.IMAGE_ORIGINAL == image_base64
