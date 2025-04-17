import os
import shutil
import re
import hashlib
import tempfile
from io import BytesIO
import zipfile

# Step 1: Process the zip file directly sent as bytes (from main.py)
def process_zip_file(file):
    # Read file bytes from the file-like object
    zip_file_bytes = file.read()  # Read all file contents as bytes

    # Create a temporary directory to extract contents
    temp_dir = tempfile.mkdtemp()

    # Step 1.1: Extract the archive content from bytes (in memory)
    with zipfile.ZipFile(BytesIO(zip_file_bytes), 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Step 2: Move all files to a temporary folder (combined folder)
    combined_folder = tempfile.mkdtemp()

    for root, _, files in os.walk(temp_dir):
        for file in files:
            src = os.path.join(root, file)
            dest = os.path.join(combined_folder, file)
            shutil.move(src, dest)

    # Step 3: Rename files (shift digits 0→1, 9→0)
    def shift_digits(filename):
        return re.sub(r"\d", lambda x: str((int(x.group(0)) + 1) % 10), filename)

    for filename in os.listdir(combined_folder):
        old_path = os.path.join(combined_folder, filename)
        new_filename = shift_digits(filename)
        new_path = os.path.join(combined_folder, new_filename)
        os.rename(old_path, new_path)

    # Step 4: Simulate grep . * | LC_ALL=C sort | sha256sum
    def get_sorted_hash(folder):
        file_contents = []
        for filename in sorted(os.listdir(folder)):  # Sort like LC_ALL=C sort
            filepath = os.path.join(folder, filename)
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        file_contents.append(f"{filename}:{line.strip()}")
            except Exception:
                pass  # Ignore non-readable files

        # Join, hash, and return SHA-256 sum
        sorted_content = "\n".join(file_contents) + "\n"
        return hashlib.sha256(sorted_content.encode("utf-8")).hexdigest()

    # Get final hash
    final_hash = get_sorted_hash(combined_folder)

    # Clean up temporary directories
    shutil.rmtree(temp_dir)
    shutil.rmtree(combined_folder)

    return final_hash