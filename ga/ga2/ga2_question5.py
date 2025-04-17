import numpy as np
from PIL import Image
import colorsys
import re

def process_image(question, file_path):
    try:
        # Open the image file
        image = Image.open(file_path)

        # Convert image to numpy array and normalize
        rgb = np.array(image) / 255.0

        # Calculate lightness for each pixel
        lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)

        # Extract the brightness threshold from the question using regex
        match = re.search(r'lightness > (\d+\.\d+)', question)
        if match:
            threshold = float(match.group(1))
        else:
            threshold = 0.72  # Default value if not specified in the question

        # Count pixels above the threshold
        light_pixels = int(np.sum(lightness > threshold))

        return str(light_pixels)
    except Exception as e:
        return {"error": f"Error processing image: {str(e)}"}
