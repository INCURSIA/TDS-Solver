import json
from flask import jsonify
def sort_json(question):
    try:
                # Find the starting index of the JSON array
        json_start = question.index('[')
        json_end = question.index(']') + 1  # To include the closing bracket
        json_string = question[json_start:json_end]  # Extract the JSON part from the string
        json_data = json.loads(json_string)  # Parse the JSON string into a Python list of dictionaries
    except (ValueError, json.JSONDecodeError):
        return jsonify({"error": "Invalid JSON format in the question"}), 400
    sorted_data = sorted(json_data, key=lambda x: (x['age'], x['name']))
    # Convert the sorted data back to JSON format
    sorted_json = json.dumps(sorted_data)
    return (sorted_json)

