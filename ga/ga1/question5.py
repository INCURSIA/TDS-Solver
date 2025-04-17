import re
import numpy as np

def solve_excel_formula(question):
    # Extract values inside SORTBY using regex
    match = re.search(r"SORTBY\(\{([\d,]+)\}, \{([\d,]+)\}\)", question)
    if not match:
        return {"error": "Invalid formula format"}
    
    values = list(map(int, match.group(1).split(',')))
    sort_keys = list(map(int, match.group(2).split(',')))

    # Extract "TAKE" parameter (N elements to take)
    take_match = re.search(r"TAKE\(.*?,\s*(\d+)\)", question)
    take_n = int(take_match.group(1)) if take_match else len(values)

    # Solve
    sorted_values = [x for _, x in sorted(zip(sort_keys, values))]
    selected_values = sorted_values[:take_n]
    
    return str(sum(selected_values))
