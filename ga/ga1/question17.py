import zipfile
import io

def function_name(zip_file):
    # Ensure the zip file is provided
    if not zip_file:
        return "No zip file uploaded."
    
    # Read the zip file into memory
    zip_content = zip_file.read()

    # Open the zip file from memory
    with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_ref:
        # Ensure both a.txt and b.txt exist in the zip file
        if 'a.txt' not in zip_ref.namelist() or 'b.txt' not in zip_ref.namelist():
            return "Missing a.txt or b.txt in the zip file."
        
        # Extract both files to memory and read their contents
        with zip_ref.open('a.txt') as file_a, zip_ref.open('b.txt') as file_b:
            a_lines = file_a.read().decode('utf-8').splitlines()
            b_lines = file_b.read().decode('utf-8').splitlines()

    # Compare the lines of both files
    differences = 0
    for line_a, line_b in zip(a_lines, b_lines):
        if line_a != line_b:
            differences += 1
    
    return str(differences)
