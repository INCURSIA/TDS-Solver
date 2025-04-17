import json
import re

def total_sales(file):
    total_sales = 0

    def extract_sales_from_line(line):
        """Attempt to manually extract sales value from a malformed line."""
        match = re.search(r'"sales":\s*(\d+)', line)
        if match:
            return int(match.group(1))
        else:
            return 0  # Return 0 if no match is found

    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace
        try:
            # Try to decode the JSON line
            data = json.loads(line)
            total_sales += data.get("sales", 0)
        except json.JSONDecodeError:
            # If decoding fails, extract sales manually from the corrupted line
            sales_value = extract_sales_from_line(line)
            total_sales += sales_value
            print(f"Corrupted line, sales extracted: {sales_value}")

    return str(total_sales)
