# import zipfile
# import pandas as pd
# import io

# def process_zip(file):
#     try:

#         with zipfile.ZipFile(io.BytesIO(file.read()), 'r') as zip_ref:
#             csv_filename = zip_ref.namelist()[0]  # Assume there's only one CSV
#             with zip_ref.open(csv_filename) as csv_file:
#                 df = pd.read_csv(csv_file)  # Read CSV into DataFrame

#                 if "answer" in df.columns:
#                     return df["answer"].iloc[0]  # Return first value in 'answer' column
#                 else:
#                     return "Error: Column 'answer' not found in CSV"
#     except Exception as e:
#         return f"Error processing ZIP file: {str(e)}"

import zipfile
import pandas as pd

def process_zip(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            csv_filename = zip_ref.namelist()[0]  # Assume there's only one CSV
            with zip_ref.open(csv_filename) as csv_file:
                df = pd.read_csv(csv_file)  # Read CSV into DataFrame

                if "answer" in df.columns:
                    return df["answer"].iloc[0]  # Return first value in 'answer' column
                else:
                    return "Error: Column 'answer' not found in CSV"
    except Exception as e:
        return f"Error processing ZIP file: {str(e)}"

# Example usage

