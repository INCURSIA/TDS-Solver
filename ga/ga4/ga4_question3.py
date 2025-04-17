from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from urllib.parse import quote
import requests

def run_question_server3():
    """
    Handles the Wikipedia outline logic directly when called from main.py.
    """
    async def get_country_outline(country: str):
        """
        Fetches the Wikipedia page for the given country and extracts the outline.
        """
        if not country:
            raise HTTPException(status_code=400, detail="Country parameter is required")

        def get_wikipedia_url(country: str) -> str:
            country = country.strip('"')
            return f"https://en.wikipedia.org/wiki/{quote(country.strip().replace(' ', '_'))}"

        def extract_headings_from_html(html: str) -> list:
            soup = BeautifulSoup(html, "html.parser")
            content_div = soup.find("div", class_="mw-page-container")
            if not content_div:
                return []
            headings = []
            for level in range(1, 7):
                for tag in content_div.find_all(f'h{level}'):
                    headings.append((level, tag.get_text(strip=True)))
            return headings

        def generate_markdown_outline(headings: list) -> str:
            markdown_outline = "## Contents\n\n"
            for level, heading in headings:
                markdown_outline += "#" * level + f" {heading}\n\n"
            return markdown_outline

        # Fetch the Wikipedia page
        url = get_wikipedia_url(country)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=404, detail=f"Error fetching Wikipedia page: {e}")

        # Extract headings and generate the outline
        headings = extract_headings_from_html(response.text)
        if not headings:
            raise HTTPException(status_code=404, detail="No headings found in the Wikipedia page")

        markdown_outline = generate_markdown_outline(headings)
        return JSONResponse(content={"outline": markdown_outline})

    # Return the endpoint function to be mounted dynamically in main.py
    return get_country_outline