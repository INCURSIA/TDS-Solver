import requests
import re
from typing import Optional

def get_params(question):
    regrex_patterns = {
        "city": r"(?:city|the city)\s*[:]*\s*([a-zA-Z\s]+?)(?=\s+in the country|$)",
        "country": r"(?:country|the country)\s*[:]*\s*([a-zA-Z\s]+?)(?=\s+on the|$)",
        "latitude_type": r"(?:latitude_type\s*:\s*|Value of the\s*)(minimum|maximum)\s*latitude"
    }
    parameters = {}
    for key, pattern in regrex_patterns.items():
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            parameters[key] = match.group(1).strip()
    
    # Default latitude_type to "minimum" if not found
    parameters["latitude_type"] = parameters.get("latitude_type", "minimum").lower()
    print(f"Extracted parameters: {parameters}")
    return parameters


def get_latitude(question: str) -> Optional[float]:
    """
    Fetches the minimum or maximum latitude for a given city and country using the Nominatim API.

    Parameters:
    - question (str): The input question.

    Returns:
    - Optional[float]: The requested latitude if found, otherwise None.
    """
    parameters = get_params(question)

    city = parameters.get("city")
    country = parameters.get("country")
    latitude_type = parameters.get("latitude_type", "minimum").lower()

    # Validate required parameters
    if not city:
        print("⚠ Error: 'city' is missing in parameters.")
        return None
    if not country:
        print("⚠ Error: 'country' is missing in parameters.")
        return None
    if latitude_type not in ["minimum", "maximum"]:
        print("⚠ Error: 'latitude_type' must be either 'minimum' or 'maximum'.")
        return None

    url = "https://nominatim.openstreetmap.org/search"
    headers = {
        "User-Agent": "MyApp/1.0 (your_email@example.com)"  # Replace with your actual email
    }
    params = {
        "q": f"{city}, {country}",  # Single query string
        "format": "json",
        "limit": 1,  # Get only one result
        "addressdetails": 1
    }

    try:
        # Fetch data from API
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()

        if not results:
            print("⚠ Error: No results found.")
            return None

        # Extract bounding box
        bounding_box = results[0].get("boundingbox")
        if bounding_box and len(bounding_box) == 4:
            latitude = float(bounding_box[0]) if latitude_type == "minimum" else float(bounding_box[1])
            return str(latitude)
        else:
            print("⚠ Error: Bounding box not available.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"⚠ Error: Request failed with error: {e}")
        return None