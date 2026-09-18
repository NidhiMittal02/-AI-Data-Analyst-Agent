import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_body_text_from_url(url: str) -> str:
    """
    Fetches an HTML page from the given URL and returns only the body text.
    Strips scripts, styles, and unnecessary whitespace.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    body = soup.body
    if not body:
        return "[No body content found]"

    text = body.get_text(separator="\n", strip=True)
    return text


def extract_text(html: str) -> str:
    """
    Extracts visible text content from the given HTML content.
    
    Args:
        html (str): Raw HTML source code.
    
    Returns:
        str: Cleaned text content from the HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)

def extract_links(html: str) -> list:
    """
    Extracts all hyperlinks from the given HTML content.
    
    Args:
        html (str): Raw HTML source code.
    
    Returns:
        list: A list of URLs found in the HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [a.get("href") for a in soup.find_all("a", href=True)]

def extract_images(html: str) -> list:
    """
    Extracts all image URLs from the given HTML content.
    
    Args:
        html (str): Raw HTML source code.
    
    Returns:
        list: A list of image source URLs.
    """
    soup = BeautifulSoup(html, "html.parser")
    return [img.get("src") for img in soup.find_all("img", src=True)]

def search_keywords(text: str, keyword: str) -> list:
    """
    Searches for a keyword in the given text and returns matching sentences.
    
    Args:
        text (str): The text to search within.
        keyword (str): The keyword to find.
    
    Returns:
        list: A list of sentences containing the keyword.
    """
    sentences = text.split(".")
    return [s.strip() for s in sentences if keyword.lower() in s.lower()]

def extract_tables(html: str) -> list:
    """
    Extracts all HTML tables from the given HTML content as lists of dictionaries.

    Args:
        html (str): Raw HTML source code.

    Returns:
        list: A list where each element is a table represented as a list of dictionaries
              (each dictionary is a row with column headers as keys).
    """
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    extracted = []

    for table in tables:
        df = pd.read_html(str(table))[0]  # Convert HTML table to pandas DataFrame
        extracted.append(df.to_dict(orient="records"))

    return extracted