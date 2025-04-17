import re

def generate_sql(question):
    match = re.search(r'in the\s+"?(\w+)"?', question, re.IGNORECASE)
    if match:
        ticket_type = match.group(1)
        return f"SELECT SUM(units * price) FROM tickets WHERE LOWER(TRIM(type)) = '{ticket_type.lower()}';"
    return "Ticket type not found in question."

