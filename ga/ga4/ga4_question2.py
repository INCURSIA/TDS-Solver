# import requests
# from bs4 import BeautifulSoup
# import json
# import re
# from typing import Optional

# def get_params_imdb(question: str) -> dict:
#     regex_patterns = {
#         "min_rating": r"rating\s+between\s+(\d+(\.\d+)?)\s+and\s+\d+(\.\d+)?",
#         "max_rating": r"rating\s+between\s+\d+(\.\d+)?\s+and\s+(\d+(\.\d+)?)"
#     }

#     parameters = {}

#     min_match = re.search(regex_patterns["min_rating"], question, re.IGNORECASE)
#     if min_match:
#         parameters["min_rating"] = float(min_match.group(1).strip())

#     max_match = re.search(regex_patterns["max_rating"], question, re.IGNORECASE)
#     if max_match:
#         parameters["max_rating"] = float(max_match.group(2).strip())

#     parameters["min_rating"] = parameters.get("min_rating", 3.0)
#     parameters["max_rating"] = parameters.get("max_rating", 5.0)

#     print(f"Extracted parameters: {parameters}")
#     return parameters


# def fetch_filtered_imdb_titles(question: str) -> Optional[str]:
#     parameters = get_params_imdb(question)

#     full_url = f"https://www.imdb.com/search/title/?title_type=feature&user_rating={parameters['min_rating']},{parameters['max_rating']}"
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     try:
#         response = requests.get(full_url, headers=headers)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         movies = []
#         movie_items = soup.select('div.sc-e2db8066-1.QxXCO.dli-parent')  # Updated selector

#         for item in movie_items:
#             title_element = item.select_one('div.dli-title a h3')
#             year_element = item.select_one('span.dli-title-metadata-item')
#             rating_element = item.select_one('span.ipc-rating-star--rating')

#             if title_element and year_element:
#                 link_tag = item.select_one('div.dli-title a')["href"]
#                 match = re.search(r'tt\d+', link_tag)
#                 imdb_id = match.group(0) if match else None

#                 title = title_element.get_text(strip=True)
#                 year = year_element.get_text(strip=True)
#                 rating = rating_element.get_text(strip=True) if rating_element else "N/A"

#                 try:
#                     rating_float = float(rating) if rating != "N/A" else None
#                     if rating_float and parameters['min_rating'] <= rating_float <= parameters['max_rating']:
#                         movies.append({
#                             "id": imdb_id,
#                             "title": title,
#                             "year": year,
#                             "rating": rating
#                         })
#                 except ValueError:
#                     continue

#         if not movies:
#             print("⚠ Error: No movies found within the specified rating range.")
#             return None
        
#         return json.dumps(movies, indent=2, ensure_ascii=False)

#     except requests.exceptions.RequestException as e:
#         print(f"⚠ Error: Request failed with error: {e}")
#         return None



    
# question_text = """Filter: Filter all titles with a rating between 3 and 5."""
# result = fetch_filtered_imdb_titles(question_text)
# print(result)


import requests
from bs4 import BeautifulSoup
import json
import re
from typing import Optional

def get_params_imdb(question: str) -> dict:
    regex_patterns = {
        "min_rating": r"rating\s+between\s+(\d+(\.\d+)?)\s+and\s+\d+(\.\d+)?",
        "max_rating": r"rating\s+between\s+\d+(\.\d+)?\s+and\s+(\d+(\.\d+)?)"
    }

    parameters = {}

    min_match = re.search(regex_patterns["min_rating"], question, re.IGNORECASE)
    if min_match:
        parameters["min_rating"] = float(min_match.group(1).strip())

    max_match = re.search(regex_patterns["max_rating"], question, re.IGNORECASE)
    if max_match:
        parameters["max_rating"] = float(max_match.group(2).strip())

    parameters["min_rating"] = parameters.get("min_rating", 3.0)
    parameters["max_rating"] = parameters.get("max_rating", 5.0)

    print(f"Extracted parameters: {parameters}")
    return parameters

def fetch_filtered_imdb_titles(question: str) -> Optional[str]:
    parameters = get_params_imdb(question)

    # full_url = f"https://www.imdb.com/search/title/?title_type=feature,tv_series&user_rating={parameters['min_rating']},{parameters['max_rating']}"
    full_url= f"https://www.imdb.com/search/title/?user_rating={parameters['min_rating']},{parameters['max_rating']}"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        movies = []
        movie_items = soup.select('div.ipc-metadata-list-summary-item__tc')  # Updated selector  # Updated selector
        # movie_items = soup.select('div[data-testid="title-card-container"]')


        for index, item in enumerate(movie_items):
            title_element = item.select_one('div.dli-title a h3')
            year_element = item.select_one('span.dli-title-metadata-item')
            rating_element = item.select_one('span.ipc-rating-star--rating')

            if title_element and year_element:
                link_tag = item.select_one('div.dli-title a')
                imdb_id = re.search(r'tt\d+', link_tag["href"]).group(0) if link_tag else None
                
                title = title_element.get_text(strip=True)
                year = year_element.get_text().replace('\xa0', ' ')
                rating = rating_element.get_text(strip=True) if rating_element else "N/A"
                
                print(f"Movie {index + 1}: {title} ({year}), Rating: {rating}")

                try:
                    rating_float = float(rating) if rating != "N/A" else None
                    if rating_float and parameters['min_rating'] <= rating_float <= parameters['max_rating']:
                        movies.append({
                            "id": imdb_id,
                            "title": title,
                            "year": year,
                            "rating": rating
                        })
                except ValueError:
                    continue

        if not movies:
            print("⚠ Error: No movies found within the specified rating range.")
            return None
        
        return json.dumps(movies, indent=2, ensure_ascii=False)

    except requests.exceptions.RequestException as e:
        print(f"⚠ Error: Request failed with error: {e}")
        return None