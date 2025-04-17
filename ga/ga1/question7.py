import re
from datetime import datetime, timedelta

def count_weekdays_in_range(question):
    # Extract weekday and date range from the question using regex
    match = re.search(r"How many (\w+) are there in the date range (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})\?", question)
    if not match:
        return "Invalid question format"

    weekday_name, start_date, end_date = match.groups()

    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Map weekday names to Python's weekday numbers (Monday=0, Sunday=6)
    weekdays = ["Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays"]
    if weekday_name not in weekdays:
        return "Invalid weekday"

    target_weekday = weekdays.index(weekday_name)

    # Count occurrences of the given weekday
    count = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() == target_weekday:
            count += 1
        current_date += timedelta(days=1)

    return str(count)
