import re
import json

def generate_json_body(question):
    """
    Generate JSON body for OpenAI API request based on the input question.
    """

    # Extract the model name
    model_match = re.search(r"Uses model ([\w\-]+)(?=\s*Has)", question)
    if not model_match:
        return "Error: Could not extract the model name."
    model_name = model_match.group(1)

    # Extract the system message (ensuring it captures only the intended part)
    system_message_match = re.search(r"Has a system message:\s*(.+?)\s*(?:Has a user message:|Uses structured outputs|$)", question, re.DOTALL)
    if not system_message_match:
        return "Error: Could not extract the system message."
    system_message = system_message_match.group(1).strip()

    # Extract the user message
    user_message_match = re.search(r"Has a user message:\s*(.+?)\s*(?:Uses structured outputs|with required fields:|$)", question, re.DOTALL)
    if not user_message_match:
        return "Error: Could not extract the user message."
    user_message = user_message_match.group(1).strip()

    # Extract required fields
    fields_match = re.search(r"with required fields:\s*(.*?)(?:\.|$)", question)
    if not fields_match:
        return "Error: Could not extract the required fields."

    fields_text = fields_match.group(1)
    field_pattern = r"(\w+)\s*\((\w+)\)"

    properties = {}
    required_fields = []

    for match in re.finditer(field_pattern, fields_text):
        field_name, field_type = match.groups()
        required_fields.append(field_name)

        json_type = {
            "string": "string",
            "number": "number",
            "array": "array",
            "boolean": "boolean"
        }.get(field_type.lower(), None)

        if json_type is None:
            return f"Error: Unsupported field type '{field_type}' for field '{field_name}'."

        properties[field_name] = {"type": json_type}

    if not required_fields:
        return "Error: No valid required fields found."

    # Construct the JSON schema
    schema = {
        "type": "object",
        "properties": {
            "addresses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": properties,
                    "required": required_fields,
                    "additionalProperties": False
                }
            }
        },
        "required": ["addresses"],
        "additionalProperties": False
    }

    # Construct the JSON body
    json_body = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "address_schema",
                "schema": schema,
                "strict": True
            }
        }
    }

    #return json_body  # Returning parsed JSON (not string)
    answer = json.dumps(json_body, indent=2, ensure_ascii=False)
    return answer
