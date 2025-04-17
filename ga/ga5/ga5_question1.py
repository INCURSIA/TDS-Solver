import pandas as pd
import re
from datetime import datetime

# Function to extract relevant information from the question
def extract_info_from_question(question):
    # Regex pattern to extract the product name (after 'for')
    product_pattern = r"for\s+(\w+)"
    
    # Regex pattern to extract the country name (after 'sold in')
    country_pattern = r"sold in\s+(\w+)"
    
    # Regex pattern to extract the date after 'before'
    date_pattern = r"before\s+([A-Za-z]+)\s+([A-Za-z]+)\s+(\d{2})\s+(\d{4})"  # Matches 'before Thu Oct 06 2022'

    # Extract product name
    product_match = re.search(product_pattern, question, re.IGNORECASE)
    product = product_match.group(1) if product_match else None

    # Extract country name
    country_match = re.search(country_pattern, question, re.IGNORECASE)
    country = country_match.group(1) if country_match else None

    # Extract date information
    date_match = re.search(date_pattern, question, re.IGNORECASE)
    if date_match:
        # Convert to datetime
        day = date_match.group(3)
        month = date_match.group(2)
        year = date_match.group(4)

        # Create a date string and parse it into a datetime object
        date_str = f"{month} {day}, {year}"
        extracted_date = datetime.strptime(date_str, "%b %d, %Y")

        # Extract the year, month, and day
        year = extracted_date.year
        month = extracted_date.month
        day = extracted_date.day
    else:
        extracted_date = None
        year = month = day = None

    return product, country, extracted_date, year, month, day

# Function to calculate total margin based on extracted information
def calculate_total_margin(file_object, question):
    # Extract relevant information from the question
    product, country, extracted_date, year, month, day = extract_info_from_question(question)

    # Read the Excel sheet from the file object
    df = pd.read_excel(file_object)

    # Convert 'Date' to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Standardize 'Country' column to lowercase (for matching variations like 'AE', 'UAE')
    df['Country'] = df['Country'].str.lower()

    # Filter for dates before extracted date and product contains extracted product and country contains extracted country
    filtered_data = df[
        (df['Date'] < extracted_date) &
        (df['Product/Code'].str.contains(product, case=False, na=False)) &
        (df['Country'].str.contains(r'ae|uae|united arab emirates|u.a.e.', case=False, na=False))
    ]

    # Clean 'Sales' and 'Cost' by removing non-numeric characters
    filtered_data['Sales'] = filtered_data['Sales'].replace({' USD': '', ',': ''}, regex=True)
    filtered_data['Cost'] = filtered_data['Cost'].replace({' USD': '', ',': ''}, regex=True)

    # Convert 'Sales' and 'Cost' to numeric
    filtered_data['Sales'] = pd.to_numeric(filtered_data['Sales'], errors='coerce')
    filtered_data['Cost'] = pd.to_numeric(filtered_data['Cost'], errors='coerce')

    # Drop rows with NaN in 'Sales' or 'Cost'
    filtered_data.dropna(subset=['Sales', 'Cost'], inplace=True)

    # Calculate margin (Sales - Cost)
    filtered_data['Margin'] = filtered_data['Sales'] - filtered_data['Cost']

    # Calculate total margin
    total_margin = filtered_data['Margin'].sum()

    # Ensure the result is a Python int for JSON serialization
    return str(total_margin.item()) + " USD"  # This converts int64 to native int and returns as a string with 'USD'
