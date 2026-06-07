import requests
from app.config import SERPER_API_KEY


def search_google(keyword: str, num_results: int = 10):
    """
    Use Serper API to fetch Google search results.

    Args:
        keyword: User input search keyword.
        num_results: Number of results to return.

    Returns:
        A list of search results.
    """

    if not keyword or not keyword.strip():
        raise ValueError("Keyword cannot be empty.")

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "q": keyword,
        "gl": "tw",
        "hl": "zh-tw",
        "num": num_results,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=20)

    if response.status_code != 200:
        raise Exception(f"Serper API error: {response.status_code}, {response.text}")

    data = response.json()

    organic_results = data.get("organic", [])

    results = []

    for index, item in enumerate(organic_results[:num_results], start=1):
        results.append({
            "rank": index,
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
        })

    return results