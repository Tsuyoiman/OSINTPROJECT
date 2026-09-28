"""
username.py - Investigates a public username on the Facebook clone.

Uses only publicly accessible pages/API endpoints exposed by the website.
No authentication, no MongoDB access, no injection.
"""

from urllib.parse import quote

from connection import fetch_url, TARGET_URL


def investigate_username(username):
    """
    Look up a public username and return any exposed profile information.

    The Facebook clone exposes public data through:
      - GET /publicProfile/<username>  (exact username handle, e.g. "megan_fox")
      - GET /searchUsers?q=<text>      (search by first name, last name,
        full name, username, or exact registration email)

    If the exact username lookup misses, this falls back to the search
    endpoint so a display name like "Megan Fox" can still resolve to the
    matching handle. Fields that are not available are set to
    "Not publicly available".
    """
    result = {
        "lookup": username,
        "username": username,
        "name": "Not publicly available",
        "bio": "Not publicly available",
        "job": "Not publicly available",
        "workplace": "Not publicly available",
        "college": "Not publicly available",
        "city": "Not publicly available",
        "hometown": "Not publicly available",
        "organizations": "Not publicly available",
        "clues": [],
        "posts": [],
        "connections": "Not publicly available",
        "friends": [],
        "picture": None,
        "cover": None,
        "found": False,
    }

    json_data = _get_public_profile(username)

    if json_data is None:
        # Fall back to search so names and exact registration emails can
        # resolve to the generated public username.
        match = _search_public_users(username)
        if match and match.get("username"):
            json_data = _get_public_profile(match["username"])

    if json_data:
        result["found"] = True
        _populate_from_json(result, json_data)

    return result


def search_users(query):
    """
    Public search step: GET /searchUsers?q=<query>.

    Returns a list of lightweight match dicts (first_name, last_name,
    username, ...) as exposed by the backend. Used when the student only
    has a partial clue (a name, a project, an organization) rather than an
    exact username.
    """
    url = f"{TARGET_URL}/searchUsers"
    resp = fetch_url(f"{url}?q={quote(query, safe='')}")
    if resp is None or resp.status_code != 200:
        return []
    try:
        data = resp.json()
    except ValueError:
        return []
    return data if isinstance(data, list) else []


def _get_public_profile(username):
    """Call GET /publicProfile/<username> and return parsed JSON, or None."""
    url = f"{TARGET_URL}/publicProfile/{quote(username, safe='')}"
    resp = fetch_url(url)
    if resp is None or resp.status_code != 200:
        return None
    try:
        return resp.json()
    except ValueError:
        return None


def _search_public_users(query):
    """Return the first fuzzy-search match, or None."""
    matches = search_users(query)
    return matches[0] if matches else None


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
        result["organizations_list"] = organizations
    else:
        result["organizations_list"] = []

    clues = simulation.get("clues")
    if isinstance(clues, list):
        result["clues"] = clues

    friends = data.get("friends")
    if isinstance(friends, list):
        result["connections"] = str(len(friends))
        # Keep the raw friend records (username/name/picture) so the
        # correlation feature can pivot into each related public profile.
        result["friends"] = friends

    if data.get("picture"):
        result["picture"] = data["picture"]
    if data.get("cover"):
        result["cover"] = data["cover"]

    posts = data.get("posts")
    if isinstance(posts, list):
        result["posts"] = posts