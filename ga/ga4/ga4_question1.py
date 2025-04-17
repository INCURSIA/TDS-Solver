import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from typing import Optional

def get_params(question: str) -> dict:
    """
    Extracts parameters from the input question using regex patterns.

    Parameters:
    - question (str): The input question.

    Returns:
    - dict: A dictionary containing extracted parameters.
    """
    regex_patterns = {
        "page_number": r"page(?:\s+number)?\s+(\d+)",  # Extracts page number
    }
    parameters = {}
    for key, pattern in regex_patterns.items():
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            parameters[key] = match.group(1).strip()
    
    # Default values if not found
    parameters["page_number"] = parameters.get("page_number", "0")
    print(f"Extracted parameters: {parameters}")
    return parameters

def get_total_ducks(question: str) -> Optional[dict]:
    """
    Extracts data from a Cricinfo stats page and sums the values of the column named "0".

    Parameters:
    - question (str): The input question.

    Returns:
    - Optional[dict]: A dictionary containing the sum of the column "0"'s values.
    """
    parameters = get_params(question)

    base_url = "https://stats.espncricinfo.com/stats/engine/stats/index.html"
    column_name = "0"  # Fixed column name
    page_number = parameters.get("page_number")

    # Validate required parameters
    if not base_url:
        print("⚠ Error: 'url' is missing in parameters.")
        return None

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    }

    params = {
        "class": 2,  # ODI format
        "template": "results",
        "type": "batting",
        "page": page_number
    }

    try:
        # Step 1: Fetch the webpage
        response = requests.get(base_url, params=params, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table", class_="engineTable")

        if len(tables) < 3:
            print("⚠ Error: Expected batting stats table not found.")
            return None

        stats_table = tables[2]  # Usually the main player stats table

        headers = [th.text.strip() for th in stats_table.find_all("th")]
        if not headers:
            print("⚠ Error: No headers found.")
            return None

        # Extract rows
        data_rows = stats_table.find_all("tr", class_="data1")
        data = []

        for row in data_rows:
            cells = [td.text.strip() for td in row.find_all("td")]
            if len(cells) == len(headers):
                data.append(cells)

        if not data:
            print("⚠ Error: No valid data rows.")
            return None

        df = pd.DataFrame(data, columns=headers)

        # Find target column
        if column_name not in df.columns:
            print(f"❌ Column '{column_name}' not found in table.")
            print(f"📊 Available columns: {list(df.columns)}")
            return None

        # Clean and convert column
        df[column_name] = df[column_name].replace({'–': '0', '-': '0', '': '0'}).astype(str)
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(0)

        total = int(df[column_name].sum())
        return str(total)

    except requests.exceptions.RequestException as e:
        print(f"⚠ Error: Request failed with error: {e}")
        return None