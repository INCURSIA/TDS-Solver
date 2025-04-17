import pandas as pd
from phonetics import dmetaphone
from rapidfuzz import process, fuzz
import re

def count_food_sales(file, question):
    # Step 1: Load the JSON data
    try:
        data = pd.read_json(file)
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {e}")

    # Fill missing cities with placeholder
    data['city'] = data['city'].fillna("Unknown")

    # Step 2: Extract food item, city, and min sales from the question
    food_item, city_input, min_sales = extract_details_from_question(question)

    if not food_item or not city_input or min_sales is None:
        raise ValueError("Could not extract valid details from the question.")

    # Predefined alternative spellings for Jakarta
    jakarta_alternatives = [
        "Jakarta", "Jakkarta", "Jakarata", "Djakarta", "Jayakarta", "Batavia"
    ]

    # Step 3: Create phonetic keys for all cities
    def get_phonetic_key(city):
        try:
            key1, key2 = dmetaphone(city)
            return key1 or key2  # Use the first key if available, otherwise the second
        except Exception:
            return None  # Handle cases where phonetic keys cannot be generated

    data['phonetic_key'] = data['city'].apply(get_phonetic_key)

    # Step 4: Fuzzy match cities to handle cases where phonetic keys differ significantly
    unique_cities = data['city'].unique().tolist()
    
    def cluster_city(city_name):
        # Step 1: Check predefined alternatives first
        for alt in jakarta_alternatives:
            if fuzz.token_sort_ratio(city_name.lower(), alt.lower()) >= 90:
                return alt
        
        # Step 2: Try phonetic matching
        phonetic_key = get_phonetic_key(city_name)
        if phonetic_key:
            matched_cities = data[data['phonetic_key'] == phonetic_key]['city'].unique()
            if len(matched_cities) > 0:
                return matched_cities[0]  # Return first match from phonetic clustering
        
        # Step 3: Use fuzzy matching as fallback
        best_match, score, _ = process.extractOne(city_name, unique_cities, scorer=fuzz.token_sort_ratio)
        return best_match if score >= 80 else city_name

    # Apply clustering logic to all cities in the dataset
    data['clustered_city'] = data['city'].apply(cluster_city)

    # # Debugging output to verify clustering
    # print("City Clustering:")
    # print(data[['city', 'phonetic_key', 'clustered_city']])

    # Step 5: Map the input city to its clustered value
    clustered_city_input = cluster_city(city_input)

    # # Debugging output for clustered input city
    # print(f"Clustered Input City: {clustered_city_input}")

    # Step 6: Filter data based on product and sales threshold
    filtered_data = data[
        (data['product'].str.lower() == food_item.lower()) &
        (data['sales'] >= min_sales)
    ]

    # # Debugging output for filtered data
    # print("Filtered Data:")
    # print(filtered_data)

    # Step 7: Group by clustered city name and calculate total sales
    grouped = filtered_data.groupby('clustered_city')['sales'].sum().reset_index()

    # # Debugging output for grouped data
    # print("Grouped Data:")
    # print(grouped)

    # Step 8: Return sales for the clustered city of the input city
    sales_in_city = grouped[grouped['clustered_city'].str.lower() == clustered_city_input.lower()]['sales'].sum()
    
    result= int(sales_in_city)
    return str(result)
import re

def extract_details_from_question(question):
    """
    Extracts details such as food item, city name, and minimum sales threshold from the question.
    
    Example Questions:
      1. "How many units of Soap were sold in London on transactions with at least 189 units?"
      2. "How many units of Pizza were sold in Lagos on transactions with at least 54 units?"
      3. "How many units of Fish were sold in Lagos on transactions with at least 199 units?"
    
    Returns:
      food_item (str): The product being queried (e.g., "Fish").
      city (str): The city being queried (e.g., "Jakarta").
      min_sales (int): The minimum sales threshold (e.g., 199).
    """
    
    food_item_match = re.search(r"units of\s+([\w\s]+?)\s+were", question, re.IGNORECASE)
    food_item = food_item_match.group(1).strip() if food_item_match else None

    city_match = re.search(r"sold in\s+([\w\s]+?)\s+on", question, re.IGNORECASE)
    city = city_match.group(1).strip() if city_match else None

    min_sales_match = re.search(r"at\s+least\s+(\d+)", question, re.IGNORECASE)
    min_sales = int(min_sales_match.group(1)) if min_sales_match else None

    return food_item, city, min_sales



