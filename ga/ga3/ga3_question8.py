from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import re

# Define the request model (if needed)
class QueryRequest(BaseModel):
    q: str

def run_question_server8():
    """
    Handles the query logic directly when called from main.py.
    """
    async def execute_query(q: str):
        """
        Processes the query and returns the appropriate response.
        """
        try:
            query = q.lower()

            # Ticket status
            match = re.search(r"status.*ticket\s+(\d+)", query)
            if match:
                ticket_id = int(match.group(1))
                return {
                    "name": "get_ticket_status",
                    "arguments": json.dumps({"ticket_id": ticket_id})
                }

            # Schedule meeting
            match = re.search(r"schedule.*?on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2}).*room\s+([a-z0-9]+)", query)
            if match:
                date = match.group(1)
                time = match.group(2)
                meeting_room = f"Room {match.group(3).capitalize()}"
                return {
                    "name": "schedule_meeting",
                    "arguments": json.dumps({"date": date, "time": time, "meeting_room": meeting_room})
                }

            # Expense balance
            match = re.search(r"expense.*employee\s+(\d+)", query)
            if match:
                employee_id = int(match.group(1))
                return {
                    "name": "get_expense_balance",
                    "arguments": json.dumps({"employee_id": employee_id})
                }

            # Performance bonus
            match = re.search(r"bonus.*employee\s+(\d+).*?(2024|2025)", query)
            if match:
                employee_id = int(match.group(1))
                current_year = int(match.group(2))
                return {
                    "name": "calculate_performance_bonus",
                    "arguments": json.dumps({"employee_id": employee_id, "current_year": current_year})
                }

            # Office issue
            match = re.search(r"issue\s+(\d+).*?(?:for|to)\s+the\s+([a-z]+)", query)
            if match:
                issue_code = int(match.group(1))
                department = match.group(2).capitalize()
                return {
                    "name": "report_office_issue",
                    "arguments": json.dumps({"issue_code": issue_code, "department": department})
                }

            # If no patterns match, raise an error
            raise HTTPException(status_code=400, detail=f"No match for query: '{q}'")

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Return the endpoint function to be mounted dynamically in main.py
    return execute_query




