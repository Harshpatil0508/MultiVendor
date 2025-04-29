from django.core.exceptions import ValidationError
import os

def allow_only_images(value):
    """
    Validate that the uploaded file is an image.
    """
    ext = os.path.splitext(value.name)[1]  # Get the file extension, cover-image.jpg, extension-> .jpg
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']

    if ext.lower() not in valid_extensions:
        raise ValidationError("Unsupported file extension. Only .jpg, .jpeg, .png, and .gif files are allowed.")
    