import re
import feedparser

def get_params_hackernews(question: str) -> dict:
    """
    Extracts the topic and minimum points from the input question using regex.

    Parameters:
    - question (str): The input question.

    Returns:
    - dict: A dictionary containing the extracted topic and minimum points.
    """
    regex_pattern = r"mentioning\s+([A-Za-z0-9]+)\s+(?:and\s+)?having\s+(?:at\s+least\s+|a\s+minimum\s+of\s+)(\d+)\s+points"
    match = re.search(regex_pattern, question, re.IGNORECASE)
    if match:
        topic = match.group(1).strip()
        min_points = int(match.group(2).strip())
        return {"topic": topic, "min_points": min_points}
    else:
        raise ValueError("Topic and minimum points could not be extracted from the question.")

def get_latest_post_link(question: str) -> str:
    """
    Fetches the link to the latest Hacker News post based on the extracted topic and minimum points.

    Parameters:
    - question (str): The input question.

    Returns:
    - str: The link to the most relevant post or an error message.
    """
    try:
        # Extract topic and minimum points from the question
        params = get_params_hackernews(question)
        topic = params["topic"]
        min_points = params["min_points"]

        # Define the HNRSS feed URL with the required parameters
        hnrss_url = f"https://hnrss.org/newest?q={topic}&points={min_points}"

        # Parse the RSS feed
        feed = feedparser.parse(hnrss_url)

        # Extract the link of the most relevant post
        if feed.entries:
            # Assuming the first entry is the most recent
            most_relevant_post_link = feed.entries[0].link
        else:
            most_relevant_post_link = "No post found with the given criteria."

        return most_relevant_post_link

    except Exception as e:
        return f"Error: {str(e)}"