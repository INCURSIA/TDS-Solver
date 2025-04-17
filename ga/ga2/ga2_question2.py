import base64
from io import BytesIO
from PIL import Image
import re

def compress_image_to_base64(question, image_path):
    """
    Compresses an image losslessly to ensure its size is less than the specified size
    from the question and returns the result as a Base64-encoded binary string
    with a data URI scheme for direct use in browsers.

    Args:
        question (str): The input question containing the target size in bytes.
        image_path (str): The file path of the image to be compressed.

    Returns:
        str: Base64-encoded binary string of the compressed image with a data URI scheme
             or an error message.
    """
    # Extract the target size from the question using regex
    match = re.search(r"less than\s*([\d,]+)\s*bytes", question, re.IGNORECASE)
    if not match:
        return "Error: Could not extract the target size from the question."

    # Remove commas from the extracted size and convert to integer
    target_size = int(match.group(1).replace(",", ""))

    # Open the image using Pillow
    with Image.open(image_path) as img:
        # Save the image to a BytesIO buffer with lossless compression
        buffer = BytesIO()
        img.save(buffer, format="PNG", optimize=True)

        # If the image size is already less than the target size, encode it directly
        if buffer.tell() < target_size:
            buffer.seek(0)
            base64_encoded = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{base64_encoded}"

        # Attempt to save the image in a more efficient lossless format (e.g., WebP)
        buffer = BytesIO()
        img.save(buffer, format="WEBP", lossless=True)

        # Check if the WebP image meets the size requirement
        if buffer.tell() < target_size:
            buffer.seek(0)
            base64_encoded = base64.b64encode(buffer.read()).decode('utf-8')
            output = f"data:image/webp;base64,{base64_encoded}"
            return output

        # If still too large, return an error
        return "Error: Unable to compress the image to the target size without loss."