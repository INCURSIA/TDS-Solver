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

    Parameters:
    - question (str): The input question.

    Returns:
    - str: The extracted email address.
    """
    regex_pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    match = re.search(regex_pattern, question)
    if match:
        return match.group(0).strip()
    else:
        raise ValueError("Email could not be extracted from the question.")

def create_daily_commit_repo(question: str):
    """
    Creates a GitHub repository with a daily commit workflow and triggers it.

    Parameters:
    - question (str): The input question containing the email.
    """
    # Extract email from the question
    email = get_email_from_question(question)

    # GitHub username and token
    username = "21f3001076"  # Replace with your GitHub username
    github_token = ""  # Replace with your GitHub token

    # Repository name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    repo_name = f"daily-commit-{timestamp}"

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

    # Create a temporary directory for the repository
    temp_dir = tempfile.mkdtemp()

    # Clone the repository using GitPython
    clone_url = f"https://{username}:{github_token}@github.com/{username}/{repo_name}.git"
    repo = Repo.clone_from(clone_url, temp_dir)

    # Create workflow directory
    workflow_dir = os.path.join(temp_dir, ".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)

    # Workflow file content
    workflow_content = f"""
name: Daily Commit

on:
  schedule:
    - cron: '30 2 * * *'
  workflow_dispatch:

jobs:
  commit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure Git ({email})
        run: |
          git config user.name "{username}"
          git config user.email "{email}"

      - name: Make daily commit
        run: |
          echo "Last run: $(date) $RANDOM" > last_run.txt
          git add last_run.txt
          git commit -m "Daily commit on $(date) $RANDOM" || echo "No changes to commit"
          git push
"""

    # Write workflow file
    workflow_file = os.path.join(workflow_dir, "daily-commit.yml")
    with open(workflow_file, "w") as f:
        f.write(workflow_content)

    # Commit and push the changes using GitPython
    repo.git.add(A=True)
    repo.index.commit("Add daily-commit workflow")
    origin = repo.remote(name="origin")
    origin.push()

    print("Committed and pushed workflow.")

    # Wait a bit for workflow indexing
    print("Waiting for GitHub to index workflow...")
    time.sleep(5)

    # Get default branch name
    repo_info = requests.get(
        f"https://api.github.com/repos/{username}/{repo_name}",
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    ).json()
    default_branch = repo_info.get("default_branch", "main")

    # Get workflow ID
    workflow_list = requests.get(
        f"https://api.github.com/repos/{username}/{repo_name}/actions/workflows",
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    ).json()

    workflow_id = None
    for wf in workflow_list.get("workflows", []):
        if wf["name"] == "Daily Commit":
            workflow_id = wf["id"]
            break

    if workflow_id is None:
        raise Exception("❌ Workflow not found!")

    # Dispatch the workflow
    dispatch_url = f"https://api.github.com/repos/{username}/{repo_name}/actions/workflows/{workflow_id}/dispatches"
    dispatch_response = requests.post(
        dispatch_url,
        headers={
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        },
        json={"ref": default_branch}
    )

    if dispatch_response.status_code == 204:
        print("Workflow dispatched successfully!")
    else:
        print(f"Failed to dispatch workflow: {dispatch_response.status_code}, {dispatch_response.text}")

    # Wait a little before making post-dispatch commit
    print("Waiting a few seconds before pushing another commit to ensure GitHub tracks it...")
    time.sleep(10)

    # Second push to ensure a commit is made after workflow runs
    with open(os.path.join(temp_dir, "ping.txt"), "w") as f:
        f.write(f"Post-dispatch commit at {datetime.utcnow().isoformat()} UTC\n")

    # Commit and push the changes using GitPython
    repo.git.add(A=True)
    repo.index.commit("post dispatch commit")
    origin = repo.remote(name="origin")
    origin.push()
    print("Post-dispatch commit pushed.")
    # Clean up the temporary directory
    shutil.rmtree(temp_dir, ignore_errors=True)

    print(f"Your repo: https://github.com/{username}/{repo_name}")
    return f"https://github.com/{username}/{repo_name}"