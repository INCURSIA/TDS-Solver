import zipfile
import io
from datetime import datetime
import pytz
import re

def extract_values_from_question(question):
    size_match = re.search(r"(\d+)\s*bytes", question)

    date_match = re.search(
        r"(\w{3},?\s*\d{1,2}\s+\w{3},?\s*\d{4},?\s*\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)\s*IST)",
        question
    )

    if not size_match or not date_match:
        return None, None

    size_threshold = int(size_match.group(1))
    date_str = date_match.group(1)

    ist = pytz.timezone("Asia/Kolkata")

    # Normalize date string to ensure consistent format
    date_str = date_str.replace(",", "")

    try:
        date_obj = datetime.strptime(date_str, "%a %d %b %Y %I:%M %p IST")
    except ValueError:
        return None, None  # Return None if parsing fails

    # Apply timezone only if naive
    if date_obj.tzinfo is None:
        date_obj = ist.localize(date_obj)

    return size_threshold, date_obj

def process_zip(zip_file, question):
    if not zip_file:
        return "No zip file uploaded."

    size_threshold, cutoff_datetime = extract_values_from_question(question)

    if size_threshold is None or cutoff_datetime is None:
        return "Error: Could not extract values from the question."

    try:
        zip_content = zip_file.read()
        if not zip_content:
            return "Error: Empty zip file."

        with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_ref:
            total_size = 0
            ist = pytz.timezone("Asia/Kolkata")

            for file_info in zip_ref.infolist():
                file_size = file_info.file_size
                file_modified_time = datetime(*file_info.date_time, tzinfo=pytz.utc).astimezone(ist)

                if file_size >= size_threshold and file_modified_time >= cutoff_datetime:
                    total_size += file_size

        return str(total_size)

    except zipfile.BadZipFile:
        return "Error: Invalid zip file."

    except Exception as e:
        return f"Unexpected error: {str(e)}"
