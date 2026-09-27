"""
connection.py - Handles HTTP communication with the target Facebook clone.
Uses only the normal web interface. No direct MongoDB access.
"""

import requests
from config import TARGET_URL

# Set a reasonable timeout so the program does not hang
REQUEST_TIMEOUT = 10

# A standard browser User-Agent so the server treats us like a normal visitor
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def get_session():
    """Return a configured requests.Session for reuse."""
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def check_connection():
    """
    Test whether the target website is reachable.
    Returns (reachable: bool, status_code: int | None, reason: str | None)
    """
    session = get_session()
    try:
        resp = session.get(TARGET_URL, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        if resp.status_code == 200:
            return True, resp.status_code, None
        return False, resp.status_code, f"HTTP {resp.status_code}"
    except requests.exceptions.Timeout:
        return False, None, "Connection timed out"
    except requests.exceptions.ConnectionError as e:
        return False, None, f"Connection error: {e}"
    except requests.exceptions.RequestException as e:
        return False, None, f"Request failed: {e}"


def fetch_url(url):
    """
    Fetch a URL and return the response object, or None on failure.
    """
    session = get_session()
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        return resp
    except requests.exceptions.RequestException:
        return None