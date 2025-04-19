import subprocess
import os
import requests

def solve_question(file_path):

    # Read the README.md content
    with open(file_path, "r") as file:
        content = file.read()

    url = "https://question3.vercel.app"  # Replace with your Vercel API URL
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json={"content": content}, headers=headers)

    if response.status_code == 200:
        print("Hashed Output:", response.json().get("hashedOutput"))
        return response.json().get("hashedOutput")
    else:
        print(f"Error: {response.status_code}")
