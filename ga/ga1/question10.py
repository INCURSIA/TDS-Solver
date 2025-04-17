import requests
import json

# Read the file

def main(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    # Convert key=value pairs to dictionary
    data = {}
    for line in lines:
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)  # Split only at the first '='
            data[key.strip()] = value.strip()

    # The data here is already a Python dictionary, which is what you want to send
    # Convert dictionary to JSON string when sending to Vercel (requests handles that automatically)
    url = "vercel_url"  # Replace with your Vercel API URL
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)  # Use json=data to send as JSON

    if response.status_code == 200:
        print("Hashed Output from JS:", response.json().get("hashedValue"))
        return response.json().get("hashedValue")
    else:
        print(f"Error: {response.status_code}")
