import re
import json

def output(question):
    # Extract email using regex
    match = re.search(r'email set to (\S+)', question)
    if match:
        email = match.group(1)
        response = {
            "args": {"email": email},
            "headers": {
                "Accept": "*/*",
                "Host": "httpbin.org",
                "User-Agent": "HTTPie/<version>"
            },
            "origin": "<your-ip-address>",
            "url": f"https://httpbin.org/get?email={email}"
        }
        return json.dumps(response, indent=2) # convert to JSON string with indentation
    return "Invalid input"

