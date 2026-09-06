import cv2
import numpy as np
import pytesseract
from PIL import Image


def preprocess_image(image):
    """
    Preprocess product package image to improve OCR accuracy.
    """

    # Convert PIL Image to OpenCV format
    if isinstance(image, Image.Image):
        image = np.array(image)

    # Convert RGB to BGR if needed
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Resize image for better OCR
    height, width = image.shape[:2]

    scale = 2

    image = cv2.resize(
        image,
        (width * scale, height * scale),
        interpolation=cv2.INTER_CUBIC
    )

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Reduce noise
    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # Improve contrast
    gray = cv2.convertScaleAbs(
        gray,
        alpha=1.5,
        beta=10
    )

    return gray


def extract_text(image):
    """
    Extract text from a product package image using OCR.
    """

    try:

        # Preprocess image
        processed_image = preprocess_image(image)

        # OCR Configuration
        custom_config = r'--oem 3 --psm 6'

        # Extract text
        text = pytesseract.image_to_string(
            processed_image,
            config=custom_config
        )

        # If OCR result is too small, try another mode
        if len(text.strip()) < 20:

            custom_config = r'--oem 3 --psm 11'

            text = pytesseract.image_to_string(
                processed_image,
                config=custom_config
            )

        return text

    except Exception as e:

        return f"OCR Error: {str(e)}"