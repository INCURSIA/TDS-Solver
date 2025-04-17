# import gzip
# import re
# from datetime import datetime
# import os

# # Define regex to capture the required parameters
# regex = r"successful (?P<method>\S+) requests for pages under (?P<directory>\S+) from (?P<start_hour>\d+):\d+ until before (?P<end_hour>\d+):\d+ on (?P<day_of_week>\w+)"

# # Apache log regex pattern
# log_pattern = re.compile(
#     r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
#     r'(?P<status>\d+) (?P<size>\S+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
# )

# # Function to extract parameters from the question
# def extract_parameters_from_question(question):
#     match = re.search(regex, question)
#     if match:
#         method = match.group("method")  # Extracts GET
#         url_prefix = match.group("url_prefix")  # Extracts /telugu/
#         start_hour = int(match.group("start_hour"))  # Extracts start hour (5)
#         end_hour = int(match.group("end_hour"))  # Extracts end hour (10)
#         day_of_week = match.group("day_of_week")  # Extracts day (Saturday)

#         # Map the extracted day to a weekday number (0 = Monday, 6 = Sunday)
#         day_map = {
#             "Mondays": 0, "Tuesdays": 1, "Wednesdays": 2, "Thursdays": 3,
#             "Fridays": 4, "Saturdays": 5, "Sundays": 6
#         }
#         target_weekday = day_map.get(day_of_week, None)

#         # Return the extracted parameters
#         return {
#             "method": method,
#             "url_prefix": url_prefix,
#             "start_hour": start_hour,
#             "end_hour": end_hour,
#             "day_of_week": day_of_week,
#             "target_weekday": target_weekday
#         }
#     else:
#         return None


# # Function to count successful GET requests based on target conditions
# def count_successful_telugu_requests(file_path, target_method, target_url_prefix, target_status_range, target_hours, target_weekday):
#     try:
#         successful_get_requests = 0

#         # Open the GZipped log file directly from the file path
#         with gzip.open(file_path, mode="rt", encoding="utf-8") as log_file:
#             for line in log_file:
#                 match = log_pattern.match(line)
#                 if match:
#                     log_data = match.groupdict()
#                     method = log_data["method"]
#                     url = log_data["url"]
#                     status = int(log_data["status"])
#                     timestamp_str = log_data["timestamp"].split(" ")[0]  # Remove timezone

#                     # Convert timestamp to datetime object
#                     log_time = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")

#                     # Check conditions: Method, URL, Status, Day (Saturday), Time (10:00 - 16:59)
#                     if (
#                         method == target_method and
#                         url.startswith(target_url_prefix) and
#                         target_status_range[0] <= status <= target_status_range[1] and
#                         log_time.weekday() == target_weekday and  # Saturday
#                         log_time.hour in target_hours  # Between 10:00 AM and 4:59 PM, based on target_hours
#                     ):
#                         successful_get_requests += 1

#         return {"successful_get_requests": successful_get_requests}

#     except Exception as e:
#         return {"error": str(e)}


# # Main function that processes the question and runs the log analysis
# def process_question_and_count_requests(question, log_file_path):
#     # Extract parameters from the question
#     params = extract_parameters_from_question(question)

#     if params:
#         # Prepare parameters for log processing
#         target_url_prefix = params["url_prefix"]
#         target_method = params["method"]
#         target_status_range = (200, 299)  # Successful requests
#         target_hours = range(params["start_hour"], params["end_hour"])  # From 10 AM to before 5 PM
#         target_weekday = params["target_weekday"]  # 5 for Saturday

#         # Run the log processing function with the extracted parameters

#         result = count_successful_telugu_requests(log_file_path, target_method, target_url_prefix, target_status_range, target_hours, target_weekday)

#         return result.get('successful_get_requests', 0)


import gzip
import re
from datetime import datetime
import os

# Define regex to capture the required parameters
regex = r"successful (?P<method>\S+) requests for pages under (?P<url_prefix>/\S+) from (?P<start_hour>\d+):\d+ until before (?P<end_hour>\d+):\d+ on (?P<day_of_week>\w+)"

# Apache log regex pattern
log_pattern = re.compile(
    r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>[^"]+)" '
    r'(?P<status>\d+) (?P<size>\S+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"'
)

# Function to extract parameters from the question
def extract_parameters_from_question(question):
    match = re.search(regex, question)
    if match:
        method = match.group("method")  # Extracts GET
        url_prefix = match.group("url_prefix")  # Extracts /telugu/
        start_hour = int(match.group("start_hour"))  # Extracts start hour (5)
        end_hour = int(match.group("end_hour"))  # Extracts end hour (10)
        day_of_week = match.group("day_of_week")  # Extracts day (Saturday)

        # Map the extracted day to a weekday number (0 = Monday, 6 = Sunday)
        day_map = {
            "Mondays": 0, "Tuesdays": 1, "Wednesdays": 2, "Thursdays": 3,
            "Fridays": 4, "Saturdays": 5, "Sundays": 6
        }
        target_weekday = day_map.get(day_of_week, None)

        # Return the extracted parameters
        return {
            "method": method,
            "url_prefix": url_prefix,
            "start_hour": start_hour,
            "end_hour": end_hour,
            "day_of_week": day_of_week,
            "target_weekday": target_weekday
        }
    else:
        return None


# Function to count successful GET requests based on target conditions
def count_successful_telugu_requests(file_path, target_method, target_url_prefix, target_status_range, target_hours, target_weekday):
    try:
        successful_get_requests = 0

        # Open the GZipped log file directly from the file path
        with gzip.open(file_path, mode="rt", encoding="utf-8") as log_file:
            for line in log_file:
                match = log_pattern.match(line)
                if match:
                    log_data = match.groupdict()
                    method = log_data["method"]
                    url = log_data["url"]
                    status = int(log_data["status"])
                    timestamp_str = log_data["timestamp"].split(" ")[0]  # Remove timezone

                    # Convert timestamp to datetime object
                    log_time = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")

                    # Check conditions: Method, URL, Status, Day (Saturday), Time (10:00 - 16:59)
                    if (
                        method == target_method and
                        url.startswith(target_url_prefix) and
                        target_status_range[0] <= status <= target_status_range[1] and
                        log_time.weekday() == target_weekday and  # Saturday
                        log_time.hour in target_hours  # Between 10:00 AM and 4:59 PM, based on target_hours
                    ):
                        successful_get_requests += 1

        return {"successful_get_requests": successful_get_requests}

    except Exception as e:
        return {"error": str(e)}


# Main function that processes the question and runs the log analysis
def process_question_and_count_requests(question, log_file_path):
    # Extract parameters from the question
    params = extract_parameters_from_question(question)

    if params:
        # Prepare parameters for log processing
        target_url_prefix = params["url_prefix"]
        target_method = params["method"]
        target_status_range = (200, 299)  # Successful requests
        target_hours = range(params["start_hour"], params["end_hour"])  # From 10 AM to before 5 PM
        target_weekday = params["target_weekday"]  # 5 for Saturday

        # Run the log processing function with the extracted parameters

        result = count_successful_telugu_requests(log_file_path, target_method, target_url_prefix, target_status_range, target_hours, target_weekday)

        result= result.get('successful_get_requests', 0)
        return str(result)





