import json
import re
import os

# Function to recursively count occurrences of a key that matches a regex pattern in the JSON structure
def count_dynamic_key(data, key_pattern):
    count = 0
    pattern = re.compile(key_pattern)  # Compile the pattern for regex matching

    # If the data is a dictionary, check each key
    if isinstance(data, dict):
        for key, value in data.items():
            if pattern.match(key):  # Match any key that fits the regex pattern
                count += 1  # Increment count if the key matches the pattern
            count += count_dynamic_key(value, key_pattern)  # Recursively check the value

    # If the data is a list, check each element
    elif isinstance(data, list):
        for item in data:
            count += count_dynamic_key(item, key_pattern)  # Recursively check each item

    return count

# Function to extract the key dynamically from the question
def extract_key_from_question(question):
    key_pattern = r'How many times does (\w+)'  # Capture the word after "How many times does"
    match = re.search(key_pattern, question)

    if match:
        return match.group(1)  # Return the captured word (the key)
    else:
        return None  # Return None if no key is found

# Main function to process the data and count the key occurrences
def process_data(file, question):
    """Processes the data from a file object and counts the occurrences of the key extracted from the question."""
    
    try:
        # Assuming file is passed as a file object, not file path
        data = json.load(file)
    except Exception as e:
        return f"Error reading file: {e}"

    # Extract the key pattern from the question
    key_pattern = extract_key_from_question(question)

    if key_pattern:
        key_pattern = re.escape(key_pattern)  # Escape any special regex characters in the key
        key_count = count_dynamic_key(data, key_pattern)  # Count occurrences of the key
        return str(key_count)
    else:
        return 0  # If no key is found in the question, return 0
