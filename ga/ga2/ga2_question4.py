import re
import hashlib
from datetime import datetime

def extract_email_hash(question: str) -> dict:
    # Step 1: Extract email using regex
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", question)
    if not match:
        return {"error": "No valid email address found in the question."}

    email = match.group(0)
    
    # Step 2: Use current year instead of token expiry
    current_year = datetime.now().year
    
    # Step 3: Generate hash
    combined = f"{email} {current_year}"
    hash_value = hashlib.sha256(combined.encode()).hexdigest()[-5:]
    
    return hash_value
