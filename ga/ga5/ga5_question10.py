import base64
from io import BytesIO
from PIL import Image

def image_to_base64(image_path):

    """
    Converts an image to a Base64-encoded binary string with a data URI scheme for direct use in browsers.

    Args:
        image_path (str): The file path of the image to be converted.

    Returns:
        str: Base64-encoded binary string of the image with a data URI scheme.
    """
    with Image.open(image_path) as img:
        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        img.save(buffer, format="WEBP", lossless=True)  # You can use "WEBP" or other formats as well
        buffer.seek(0)
        
        # Convert to base64
        base64_encoded = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/webp;base64,{base64_encoded}"

