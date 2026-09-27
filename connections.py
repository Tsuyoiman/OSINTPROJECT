"""
connections.py - Placeholder for future connection-graph functionality.
"""

from connection import fetch_url, TARGET_URL


def fetch_public_connections(username):
    """Fetch publicly visible connections for a username (future use)."""
    url = f"{TARGET_URL}/api/connections/{username}"
    resp = fetch_url(url)
    if resp is None:
        return "Not publicly available"
    try:
        data = resp.json()
        return data
    except ValueError:
        return "Not publicly available"