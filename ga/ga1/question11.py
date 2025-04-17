import re
from bs4 import BeautifulSoup

def output(input_data):
    # Read the HTML content from input_data (assuming it's a file-like object)
    html_content = input_data.read()
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find all <div> elements with class containing "foo"
    divs = soup.find_all("div", class_=lambda c: c and "foo" in c)
    
    # Sum up their data-value attributes
    total = sum(int(div["data-value"]) for div in divs if div.has_attr("data-value"))
    
    return str(total)  # Return the final sum of data-value attributes