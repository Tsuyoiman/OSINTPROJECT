"""
posts.py - Placeholder for future post-scraping functionality.
"""

from connection import fetch_url, TARGET_URL


def fetch_public_posts(username):
    """Fetch public posts for a username (future use)."""
    url = f"{TARGET_URL}/api/posts/{username}"
    resp = fetch_url(url)
    if resp is None:
        return []
    try:
        return resp.json()
    except ValueError:
        return []