"""
username.py - Investigates a public username on the Facebook clone.

Uses only publicly accessible pages/API endpoints exposed by the website.
No authentication, no MongoDB access, no injection.
"""

from connection import fetch_url, TARGET_URL


def investigate_username(username):
    """
    Look up a public username and return any exposed profile information.

    The Facebook clone exposes public data through:
      - GET /publicProfile/<username>  (exact username handle, e.g. "megan_fox")
      - GET /searchUsers?q=<text>      (fuzzy search by first/last name or username)

    If the exact username lookup misses, this falls back to the search
    endpoint so a display name like "Megan Fox" can still resolve to the
    matching handle. Fields that are not available are set to
    "Not publicly available".
    """
    result = {
        "username": username,
        "name": "Not publicly available",
        "bio": "Not publicly available",
        "job": "Not publicly available",
        "workplace": "Not publicly available",
        "college": "Not publicly available",
        "city": "Not publicly available",
        "hometown": "Not publicly available",
        "organizations": "Not publicly available",
        "posts": [],
        "connections": "Not publicly available",
    }

    json_data = _get_public_profile(username)

    if json_data is None:
        # Fall back to fuzzy search (handles display names / partial matches)
        match = _search_public_users(username)
        if match and match.get("username"):
            json_data = _get_public_profile(match["username"])

    if json_data:
        _populate_from_json(result, json_data)

    return result


def _get_public_profile(username):
    """Call GET /publicProfile/<username> and return parsed JSON, or None."""
    url = f"{TARGET_URL}/publicProfile/{username}"
    resp = fetch_url(url)
    if resp is None or resp.status_code != 200:
        return None
    try:
        return resp.json()
    except ValueError:
        return None


def _search_public_users(query):
    """Call GET /searchUsers?q=<query> and return the first match, or None."""
    url = f"{TARGET_URL}/searchUsers"
    resp = fetch_url(f"{url}?q={query}")
    if resp is None or resp.status_code != 200:
        return None
    try:
        data = resp.json()
    except ValueError:
        return None
    if isinstance(data, list) and data:
        return data[0]
    return None


def _populate_from_json(result, data):
    """Map the backend's public-profile JSON shape into the result dict."""
    first_name = data.get("first_name") or ""
    last_name = data.get("last_name") or ""
    full_name = f"{first_name} {last_name}".strip()
    if full_name:
        result["name"] = full_name

    if data.get("username"):
        result["username"] = data["username"]

    details = data.get("details") or {}
    detail_map = {
        "bio": "bio",
        "job": "job",
        "workplace": "workplace",
        "college": "college",
        "city": "currentCity",
        "hometown": "hometown",
    }
    for result_key, src_key in detail_map.items():
        val = details.get(src_key)
        if val:
            result[result_key] = val

    simulation = data.get("simulation") or {}
    organizations = simulation.get("organizations")
    if isinstance(organizations, list) and organizations:
        result["organizations"] = ", ".join(organizations)

    friends = data.get("friends")
    if isinstance(friends, list):
        result["connections"] = str(len(friends))

    posts = data.get("posts")
    if isinstance(posts, list):
        result["posts"] = posts