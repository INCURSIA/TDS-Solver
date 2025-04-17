import re
import numpy as np

def solve_google_sheets(question):
    print("\nReceived Question:", question)  # Debugging print

    # Fixed regex for matching Google Sheets formula
    match = re.search(
        r"SEQUENCE\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*,\s*(\d+)\s*,\s*(\d+)",
        question,
        re.IGNORECASE
    )

    if not match:
        print("❌ Regex Failed to Match!")  # Debugging print
        return "Error: Invalid formula format"

    # Extract values
    rows, cols, start, step, row_limit, col_limit = map(int, match.groups())

    print(f"✅ Extracted -> rows: {rows}, cols: {cols}, start: {start}, step: {step}, row_limit: {row_limit}, col_limit: {col_limit}")

    # Generate SEQUENCE matrix
    sequence = np.array([[start + step * j for j in range(cols)] for i in range(rows)])

    # Apply ARRAY_CONSTRAIN
    constrained_array = sequence[:row_limit, :col_limit]

    # Compute SUM
    result = np.sum(constrained_array)

    return str(result)
