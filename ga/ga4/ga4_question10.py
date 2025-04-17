import pdfplumber
import markdownify
import os
import json
import requests

def convert_pdf_to_markdown(pdf_path: str, output_md_path: str) -> str:
    """
    Converts a PDF file to Markdown, formats it using Prettier, and returns the formatted Markdown content.

    Args:
        pdf_path (str): The path to the PDF file.
        output_md_path (str): The path to save the converted Markdown file.

    Returns:
        str: The formatted Markdown content.
    """
    markdown_content = ""

    # Step 1: Extract text from PDF
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                markdown_content += markdownify.markdownify(text, heading_style="ATX") + "\n\n"

    if not markdown_content.strip():
        raise ValueError("No extractable text found in the PDF.")

    # Step 2: Save the raw Markdown content
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    # Step 3: Format the Markdown using Prettier API
    formatted_content = format_markdown_with_prettier(markdown_content)

    # Step 4: Save the formatted Markdown back to the file
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        md_file.write(formatted_content)

    return formatted_content


def format_markdown_with_prettier(markdown_content: str) -> str:
    """
    Formats Markdown content using Prettier via an HTTP request.

    Args:
        markdown_content (str): The raw Markdown content.

    Returns:
        str: The formatted Markdown content.
    """

    # 🚀 Replace this with a valid Prettier API endpoint if available.
    prettier_api_url = "https://your-prettier-api-endpoint.com/format"

    prettier_config = {
        "parser": "markdown",
        "tabWidth": 2,
        "useTabs": False,
    }

    try:
        response = requests.post(
            prettier_api_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"content": markdown_content, "options": prettier_config}),
        )
        response.raise_for_status()
        return response.json().get("formatted", markdown_content)
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Warning: Failed to format Markdown with Prettier: {e}")
        return markdown_content  # Return unformatted content if API fails


def main(pdf_path: str) -> str:
    """
    Main function to handle PDF to Markdown conversion and formatting.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        str: The formatted Markdown content.
    """

    # Define output Markdown file path
    output_md_path = os.path.splitext(pdf_path)[0] + ".md"

    # Convert and format the PDF content
    formatted_markdown = convert_pdf_to_markdown(pdf_path, output_md_path)

    return formatted_markdown
