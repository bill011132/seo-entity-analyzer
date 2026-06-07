import requests
from bs4 import BeautifulSoup


def fetch_article_text(url: str) -> str:
    """
    Fetch webpage content and extract readable text.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # Fix Chinese encoding problem
        if response.encoding is None or response.encoding.lower() == "iso-8859-1":
            response.encoding = response.apparent_encoding

    except Exception:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())

    return text