import os
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
GOOGLE_APPS_SCRIPT_URL = os.getenv("GOOGLE_APPS_SCRIPT_URL")

if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY is not set. Please add it to your .env file.")