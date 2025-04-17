import pandas as pd
import zipfile
import io
import re

# Function to extract symbols from the question using regex
def extract_symbols(question):
    matches = re.findall(r"matches\s+([\S])|OR\s+([\S])", question)
    symbols = {match[0] or match[1] for match in matches if match[0] or match[1]}
    return symbols

# Function to sum values where symbol matches extracted ones
def sum_matching_values(zip_bytes, files, question):
    # Extract symbols from the question text
    symbols = extract_symbols(question)
    total_sum = 0

    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zip_ref:
        for file, encoding in files.items():
            with zip_ref.open(file) as f:
                sep = "\t" if file.endswith(".txt") else ","
                df = pd.read_csv(f, encoding=encoding, sep=sep)

                # Sum values where symbol matches extracted ones
                total_sum += df[df["symbol"].isin(symbols)]["value"].sum()

    return int(total_sum) # Return the final sum

# --- MAIN EXECUTION --- (This would be in your main.py)
def main(zip_path, question_text):
    # Define expected file encodings
    files_info = {
        "data1.csv": "cp1252",
        "data2.csv": "utf-8",
        "data3.txt": "utf-16"
    }

    # Load ZIP file into memory
    with open(zip_path, "rb") as zip_file:
        zip_bytes = zip_file.read()

    # Compute sum without extracting files
    final_sum = sum_matching_values(zip_bytes, files_info, question_text)

    return str(final_sum)  # Return the result instead of printing it

