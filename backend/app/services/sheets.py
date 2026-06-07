import requests
from app.config import GOOGLE_APPS_SCRIPT_URL


def write_to_google_sheet(payload: dict):
    """
    Send analysis result to Google Apps Script Web App,
    then Apps Script writes data into Google Sheet.
    """

    if not GOOGLE_APPS_SCRIPT_URL:
        raise ValueError("GOOGLE_APPS_SCRIPT_URL is not set in .env")

    response = requests.post(
        GOOGLE_APPS_SCRIPT_URL,
        json=payload,
        timeout=30,
    )

    if response.status_code != 200:
        raise Exception(
            f"Google Apps Script error: {response.status_code}, {response.text}"
        )

    try:
        return response.json()
    except Exception:
        return {
            "success": False,
            "raw_response": response.text
        }