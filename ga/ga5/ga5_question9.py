import re
import pandas as pd

def get_transcript_text_with_overlap(file_path, start_time, end_time):
    """
    Filters the transcript CSV file based on the given timestamps and includes overlapping lines.
    """
    # Load the transcript CSV file
    data = pd.read_csv(file_path)

    # Filter rows where there is any overlap with the specified time range
    filtered_data = data[(data['Start (s)'] < end_time) & (data['End (s)'] > start_time)]

    # Combine the text into a single paragraph
    transcript_text = ' '.join(filtered_data['Text'].tolist())

    return transcript_text

def extract_timestamps(question):
    """
    Extracts start and end timestamps from the question.
    """
    matches = re.findall(r'between\s+(\d+(?:\.\d+)?)\s+and\s+(\d+(?:\.\d+)?)\s+seconds', question)

    #matches = re.findall(r"between (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?) seconds", question)
    if matches:
        start_time, end_time = map(float, matches[0])  # Extract first match
        return start_time, end_time
    return None, None

def process_question_and_get_transcript_with_overlap(question, file_path):
    """
    Processes the question to extract timestamps and retrieves the corresponding transcript text.
    """
    # Extract timestamps from the question
    start_time, end_time = extract_timestamps(question)

    if start_time is not None and end_time is not None:
        # Get transcript text for the extracted timestamps with overlap logic
        transcript_text = get_transcript_text_with_overlap(file_path, start_time, end_time)
        return transcript_text if transcript_text else "No transcript found for the given time range."
    
    return "Error: Could not extract timestamps from the question."
