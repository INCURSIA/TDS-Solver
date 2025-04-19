import requests
import json

def handle_vercel_deploy(file_path):

# Load the JSON file locally
    with open(file_path, "r") as file:
        json_data = json.load(file)

    # Send the JSON data to the Vercel API for storage
    upload_url = "https://question3.vercel.app"
    upload_response = requests.post(upload_url, files={"file": open(file_path, "rb")})

    if upload_response.status_code == 200:
        print("✅ File uploaded successfully!")
        url = "https://question3.vercel.app"
        return url
    else:
        print(f"❌ Upload Error: {upload_response.status_code}, {upload_response.text}")
        exit()

# # -------------------------------------------
# # *Step 2: Query for Marks After Upload*
# query_url = "vercel_url"  # Example names
# query_response = requests.get(query_url)

# # Print the response
# if query_response.status_code == 200:
#     print("✅ Query Response:", query_response.json())
# else:
#     print(f"❌ Query Error: {query_response.status_code}, {query_response.text}")




