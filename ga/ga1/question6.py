import re
import json
import os

def output(input_data):

    html_content = input_data.read() 
    match = re.search(r'<input\s+type="hidden"\s+value="([^"]+)"', html_content)
    
    if match:
        return match.group(1)
    else:
        return "Not found"
