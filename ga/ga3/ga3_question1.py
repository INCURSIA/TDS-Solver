# import re

# def generate_sentiment_analysis_code(question):
#     # Extract the meaningless text from the question
#     match = re.search(r"One of the test cases involves sending a sample piece of meaningless text:\s*([\s\S]+?)\s*Write a Python program", question)

#     if not match:
#         return '{"answer": "Error: Could not extract the meaningless text."}'

#     test_text = match.group(1).strip()

#     # Generate the required Python code
#     code = f'''
# import httpx
# API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
# HEADERS = {
#     "Authorization": "Bearer dummy_api_key",
#     "Content-Type": "application/json"
# }

# DATA = {
#     "model": "gpt-4o-mini",
#     "messages": [
#         {"role": "system", "content": "Analyze the sentiment of the following text as GOOD, BAD, or NEUTRAL."},
#         {"role": "user", "content": """{test_text}"""}
#     ]
# }

# try:
#     response = httpx.post(API_URL, json=DATA, headers=HEADERS)
#     response.raise_for_status()

#     # Parse response
#     result = response.json()
#     print(result)
# except httpx.HTTPStatusError as e:
#     print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")'''

#     # Wrap the code in a JSON-like structure
#     return code


import re
import json

def generate_sentiment_analysis_code(question):
    # Extract the meaningless text from the question
    match = re.search(r"One of the test cases involves sending a sample piece of meaningless text:\s*([\s\S]+?)\s*Write a Python program", question)

    if not match:
        return '{"answer": "Error: Could not extract the meaningless text."}'

    test_text = match.group(1).strip()

    # Generate the required Python code
    code = f'''
import httpx

url = "https://api.openai.com/v1/chat/completions"
headers = {{
    "Authorization": "Bearer dummy_api_key",
    "Content-Type": "application/json"
}}
data = {{
    "model": "gpt-4o-mini",
    "messages": [
        {{"role": "system", "content": "Analyze the sentiment of the given text and classify it as GOOD, BAD, or NEUTRAL."}},
        {{"role": "user", "content": """{test_text}"""}}
    ]
}}

response = httpx.post(url, json=data, headers=headers)
response.raise_for_status()
result = response.json()

print(result)
'''

    # Wrap the code in a JSON-like structure
    return code

