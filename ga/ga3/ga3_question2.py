import re
import tiktoken

def estimate_token_usage(question):
    """
    Extracts the user message from the question and estimates the number of tokens used.

    Args:
        question (str): The input question containing the user message.

    Returns:
        int: Accurate number of tokens for the user message using OpenAI's tokenizer.
    """
    # Extract the user message using regex
    match = re.search(
        r"Specifically, when you make a request to OpenAI's GPT-4o-Mini with just this user message:\s*(.*?)\s*\.\.\. how many input tokens does it use up\?",
        question,
        re.DOTALL
    )

    if not match:
        return "Error: Could not extract the user message."

    user_message = match.group(1).strip()

    # Load the tokenizer for GPT-4o-Mini
    enc = tiktoken.encoding_for_model("gpt-4o")  # GPT-4o-Mini uses the same encoding

    # Get the token count using tiktoken
    token_count = len(enc.encode(user_message))+7

    return str(token_count)
