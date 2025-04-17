import re
from datetime import datetime
import gzip
import os
from collections import defaultdict


# Function to extract parameters from the question and convert them
def extract_and_convert_parameters(question):
    # Define regex to capture the string after 'under' and the date after 'on'
    regex = r"under (?P<string>[\w/]+) on (?P<date>\d{4}-\d{2}-\d{2})"
    
    # Apply regex to the question
    match = re.search(regex, question)

    if match:
        # Extract the parameters using named groups
        string_param = match.group("string")
        date_param = match.group("date")
        
        # Convert string_param to start with '/'
        string_param = '/' + string_param.lstrip('/')
        
        # Convert the date to the desired format
        date_object = datetime.strptime(date_param, "%Y-%m-%d")
        formatted_date = date_object.strftime("%d/%b/%Y")  # Output format 22/May/2024

        return string_param, formatted_date
    else:
        raise ValueError("No match found in the question.")

# Function to parse logs and calculate the top bytes downloaded
def calculate_top_bytes(log_file_path, para_1, date):
    # Define regex pattern to parse log entries
    log_pattern = re.compile(
        r'(?P<ip>\S+) \S+ \S+ \[(?P<time>\d{2}/May/2024:\d{2}:\d{2}:\d{2}) [+-]\d{4}] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+) .+')

    data_usage = defaultdict(int)

    # Parse log entries
    with gzip.open(log_file_path, 'rt', encoding='utf-8') as file:
        for line in file:
            match = log_pattern.match(line)
            if match:
                ip = match.group("ip")
                time = match.group("time")
                url = match.group("url")
                status = int(match.group("status"))
                size = match.group("size")

                if size == "-":
                    size = 0
                else:
                    size = int(size)

                # Corrected date check
                if time.startswith(date) and url.startswith(para_1):
                    data_usage[ip] += size

    # Find the top IP by data usage
    top_ip = max(data_usage, key=data_usage.get, default=None)
    top_bytes = data_usage[top_ip] if top_ip else 0

    return top_bytes


# Main function to execute both operations
def main(question,log_file_path):
    # Extract parameters from the question
    string_param, formatted_date = extract_and_convert_parameters(question)

    # Calculate the top bytes downloaded
    top_bytes = calculate_top_bytes(log_file_path, string_param, formatted_date)
    
    return str(top_bytes)



