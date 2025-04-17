import re
import requests

def get_params_github(question: str) -> dict:
    """
    Extracts the city and minimum followers from the input question using regex.

    Parameters:
    - question (str): The input question.

    Returns:
    - dict: A dictionary containing the extracted city and minimum followers.
    """
    regex_pattern = r"located\s+in\s+the\s+city\s+([A-Za-z\s]+)\s+with\s+over\s+(\d+)\s+followers"
    match = re.search(regex_pattern, question, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        min_followers = int(match.group(2).strip())
        return {"city": city, "min_followers": min_followers}
    else:
        raise ValueError("City and minimum followers could not be extracted from the question.")

def get_github_users(question: str) -> str:
    """
    Fetches the creation date of the newest GitHub user based on the extracted city and minimum followers.

    Parameters:
    - question (str): The input question.

    Returns:
    - str: The ISO 8601 creation date of the newest user or an error message.
    """
    try:
        # Extract city and minimum followers from the question
        params = get_params_github(question)
        city = params["city"]
        min_followers = params["min_followers"]

        # GitHub API URL and parameters
        url = "https://api.github.com/search/users"
        query_params = {
            "q": f"location:{city} followers:>{min_followers}",
            "sort": "joined",
            "order": "desc",
            "per_page": 100  # Max results per page
        }
        headers = {"Accept": "application/vnd.github.v3+json"}

        # Make the API request
        response = requests.get(url, params=query_params, headers=headers)

        if response.status_code == 200:
            users = response.json().get("items", [])
            if users:
                newest_user = users[0]  # The first user in the sorted list is the newest
                user_details = requests.get(newest_user["url"], headers=headers).json()
                return user_details["created_at"]  # ISO 8601 format
            else:
                return "No users found with the given criteria."
        else:
            return f"Error: {response.status_code}, {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"