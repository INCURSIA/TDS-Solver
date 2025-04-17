import json
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import Optional

def get_params_weather(question: str) -> dict:
    """
    Extracts the city name from the input question using regex.

    Parameters:
    - question (str): The input question.

    Returns:
    - dict: A dictionary containing the extracted city name.
    """
    regex_pattern = r"for\s+([A-Za-z\s]+)\??$"
    match = re.search(regex_pattern, question, re.IGNORECASE)
    if match:
        city_name = match.group(1).strip()
        return {"city_name": city_name}
    else:
        raise ValueError("City name could not be extracted from the question.")

def get_bbc_weather_by_city(question: str) -> Optional[str]:
    """
    Fetches the weather forecast for a city using the BBC Weather API.

    Parameters:
    - question (str): The input question.

    Returns:
    - Optional[str]: A JSON string containing the weather forecast.
    """
    try:
        # Extract city name from the question
        params = get_params_weather(question)
        city_name = params["city_name"]

        # Build BBC location URL
        location_url = 'https://locator-service.api.bbci.co.uk/locations?' + urlencode({
            'api_key': 'AGbFAKx58hyjQScCXIYrxuEwJh2W2cmv',
            's': city_name,
            'stack': 'aws',
            'locale': 'en',
            'filter': 'international',
            'place-types': 'settlement,airport,district',
            'order': 'importance',
            'a': 'true',
            'format': 'json'
        })

        # Get location ID
        result = requests.get(location_url).json()
        location_id = result['response']['results']['results'][0]['id']
        weather_url = f'https://www.bbc.com/weather/{location_id}'

        # Fetch weather page
        response = requests.get(weather_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all daily forecast blocks
        days = soup.find_all('li', class_='wr-day')

        forecast = {}
        for day in days:
            # Get the date from aria-label
            title_div = day.find('div', class_='wr-day__title')
            if title_div and 'aria-label' in title_div.attrs:
                aria_label = title_div['aria-label']
                match = re.search(r'(\d{1,2})(st|nd|rd|th)?\s+([A-Za-z]+)', aria_label)
                if match:
                    day_str = f"{match.group(1)} {match.group(3)}"
                    # Append year and convert to YYYY-MM-DD
                    current_year = datetime.now().year
                    date_obj = datetime.strptime(f"{day_str} {current_year}", "%d %B %Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                else:
                    continue
            else:
                continue

            # Get weather description
            desc_div = day.find('div', class_='wr-day__details__weather-type-description')
            if desc_div:
                description = desc_div.text.strip()
            else:
                description = "N/A"

            forecast[formatted_date] = description

        raw_json = json.dumps(forecast, indent=4)  # Parse the JSON string to ensure it's valid
        return raw_json

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)