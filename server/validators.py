import os

from rest_framework.exceptions import ValidationError
from PIL import Image
import os


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The maximum allowed dimension for the image are 70x70px - size of image you uploaded: {image.size}"
                )


def validate_icon_image_extension(image):
    ext = os.path.splitext(image.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            f"The extension of the image must be one of the following: {valid_extensions}"
        )
