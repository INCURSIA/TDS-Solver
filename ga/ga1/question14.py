# import os
# import shutil
# import re
# import hashlib
# import tempfile
# from io import BytesIO
# import zipfile

# # Function to process the ZIP file and return the hash
# def process_zip_file(zip_file_bytes):
#     # Step 1: Create a temporary folder for extraction
#     temp_dir = tempfile.mkdtemp()

#     # Step 1.1: Extract the archive content from bytes (in memory)
#     with zipfile.ZipFile(BytesIO(zip_file_bytes), 'r') as zip_ref:
#         zip_ref.extractall(temp_dir)

#     # Step 2: Replace "IITM" (case-insensitive) with "IIT Madras" in all files
#     def replace_text_in_file(filepath):
#         with open(filepath, "rb") as f:
#             content = f.read()  # Read as bytes to preserve line endings

#         updated_content = re.sub(rb"(?i)IITM", b"IIT Madras", content)  # Case-insensitive replacement

#         if updated_content != content:  # Only write if changes were made
#             with open(filepath, "wb") as f:
#                 f.write(updated_content)

#     for root, _, files in os.walk(temp_dir):
#         for file in files:
#             replace_text_in_file(os.path.join(root, file))

#     # Step 3: Compute `cat * | sha256sum`
#     def compute_sha256(folder):
#         file_contents = []
#         for filename in sorted(os.listdir(folder)):  # Sort like Bash `cat *`
#             filepath = os.path.join(folder, filename)
#             try:
#                 with open(filepath, "rb") as f:  # Read as bytes to avoid encoding issues
#                     file_contents.append(f.read())
#             except Exception:
#                 pass  # Ignore unreadable files

#         combined_content = b"".join(file_contents)  # Simulate `cat *`
#         return hashlib.sha256(combined_content).hexdigest()

#     # Get the final hash
#     final_hash = compute_sha256(temp_dir)

#     # Clean up the temporary directory
#     shutil.rmtree(temp_dir)

#     return final_hash


import os
import shutil
import re
import hashlib
import tempfile
from io import BytesIO
import zipfile

# Function to process the ZIP file and return the hash
def process_zip_file(file, question):
    # Step 1: Create a temporary folder for extraction
    temp_dir = tempfile.mkdtemp()

    # Step 1.1: Read the file content and extract the ZIP file from disk
    # Wrap the file bytes in BytesIO to make it file-like
    with zipfile.ZipFile(BytesIO(file.read()), 'r') as zip_ref:  # Use BytesIO here
        zip_ref.extractall(temp_dir)

    # Step 2: Replace "IITM" (case-insensitive) with "IIT Madras" in all files
    def replace_text_in_file(filepath):
        with open(filepath, "rb") as f:
            content = f.read()  # Read as bytes to preserve line endings

        updated_content = re.sub(rb"(?i)IITM", b"IIT Madras", content)  # Case-insensitive replacement

        if updated_content != content:  # Only write if changes were made
            with open(filepath, "wb") as f:
                f.write(updated_content)

    # Iterate through files in the extracted ZIP and perform replacements
    for root, _, files in os.walk(temp_dir):
        for file_name in files:
            replace_text_in_file(os.path.join(root, file_name))

    # Step 3: Compute cat * | sha256sum
    def compute_sha256(folder):
        file_contents = []
        for filename in sorted(os.listdir(folder)):  # Sort like Bash cat *
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, "rb") as f:  # Read as bytes to avoid encoding issues
                    file_contents.append(f.read())
            except Exception:
                pass  # Ignore unreadable files

        combined_content = b"".join(file_contents)  # Simulate cat *
        return hashlib.sha256(combined_content).hexdigest()

    # Get the final hash
    final_hash = compute_sha256(temp_dir)

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

    return final_hash
