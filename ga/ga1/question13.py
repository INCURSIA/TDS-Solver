import os
import json
import tempfile
import shutil
import requests
import re
from datetime import datetime
from git import Repo  # GitPython library

def extract_email_from_text(text: str) -> str:
    """
    Extracts an email address from the given text using regex dynamically.
    
    Parameters:
    - text (str): The input text.
    
    Returns:
    - str: The extracted email address.
    """
    regex_pattern = r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"  # General email regex pattern
    match = re.search(regex_pattern, text)
    if match:
        return match.group(0).strip()
    else:
        raise ValueError("No email address found in the text.")

def create_github_repo_with_email(text: str) -> str:
    """
    Extracts Gmail from text, creates a GitHub repository, commits a JSON file with the extracted email, 
    and returns the raw GitHub URL.

    Parameters:
    - text (str): The input text containing an email.

    Returns:
    - str: The raw GitHub URL of the committed email.json file.
    """
    email = extract_email_from_text(text)
    username = "21f3001076"  # Replace with your GitHub username
    github_token = ""  # Replace with your GitHub token

    # Repository name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    repo_name = f"email-repo-{timestamp}"

    print(f"🔧 Creating GitHub repository: {repo_name}")
    response = requests.post(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        },
        json={"name": repo_name, "private": False}
    )
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to create repo: {response.text}")
    print("Repository created.")

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Clone the repository
    clone_url = f"https://{username}:{github_token}@github.com/{username}/{repo_name}.git"
    repo = Repo.clone_from(clone_url, temp_dir)

    # Create email.json file
    email_data = {"email": email}
    email_file_path = os.path.join(temp_dir, "email.json")
    with open(email_file_path, "w") as f:
        json.dump(email_data, f, indent=4)

    # Commit and push changes
    repo.git.add(A=True)
    repo.index.commit("Added email.json")
    origin = repo.remote(name="origin")
    origin.push()

    print("Committed and pushed email.json.")

    # Clean up temporary directory
    shutil.rmtree(temp_dir, ignore_errors=True)

    raw_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/main/email.json"
    print(f"Your raw file URL: {raw_url}")
    return raw_url


