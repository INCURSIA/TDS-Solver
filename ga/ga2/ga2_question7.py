import re
import os
import tempfile
import shutil
from datetime import datetime
import requests
import time
from git import Repo  # GitPython library

def get_email_from_question(question: str) -> str:
    """
    Extracts the email from the input question using regex.
    """
    regex_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    match = re.search(regex_pattern, question)
    if match:
        return match.group(0).strip()
    else:
        raise ValueError("Email could not be extracted from the question.")

def create_github_action_with_email(email: str):
    """
    Creates a GitHub Action workflow containing the provided email.
    """
    username = "21f3001076"  # Replace with your GitHub username
    github_token = ""  # Replace with your GitHub token
    repo_name = f"github-action-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print(f"Creating GitHub repository: {repo_name}")
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
    temp_dir = tempfile.mkdtemp()
    clone_url = f"https://{username}:{github_token}@github.com/{username}/{repo_name}.git"
    repo = Repo.clone_from(clone_url, temp_dir)
    workflow_dir = os.path.join(temp_dir, ".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    
    workflow_content = f"""
name: GitHub Action with Email

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: {email}
        run: echo "Hello, GitHub Actions!"
"""
    
    workflow_file = os.path.join(workflow_dir, "github-action.yml")
    with open(workflow_file, "w") as f:
        f.write(workflow_content)
    
    repo.git.add(A=True)
    repo.index.commit("Add GitHub Action workflow")
    repo.remote(name="origin").push()
    print("Workflow committed and pushed.")
    
    shutil.rmtree(temp_dir, ignore_errors=True)
    return f"https://github.com/{username}/{repo_name}"

def run_question_server_github(question: str):
    """
    Extracts email from the question and creates the GitHub Action workflow.
    """
    email = get_email_from_question(question)
    return create_github_action_with_email(email)
