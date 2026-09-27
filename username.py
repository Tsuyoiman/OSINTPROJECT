"""
username.py - Investigates a public username on the Facebook clone.

Uses only publicly accessible pages/API endpoints exposed by the website.
No authentication, no MongoDB access, no injection.
"""

from connection import fetch_url, TARGET_URL


def investigate_username(username):
    """
    Look up a public username and return any exposed profile information.

    The Facebook clone may expose public data through:
      - A public profile page (e.g. /profile/<username>)
      - A public JSON API endpoint (e.g. /api/users/<username>)

    This function tries the most common public routes and returns whatever
    data the website actually exposes. Fields that are not available are
    set to "Not publicly available".
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

    # Try common public profile endpoints
    candidate_paths = [
        f"/profile/{username}",
        f"/api/users/{username}",
        f"/u/{username}",
        f"/user/{username}",
    ]

    html = None
    json_data = None

    for path in candidate_paths:
        url = f"{TARGET_URL}{path}"
        resp = fetch_url(url)
        if resp is None:
            continue

        content_type = resp.headers.get("Content-Type", "").lower()

        # JSON API response
        if "application/json" in content_type:
            try:
                json_data = resp.json()
                break
            except ValueError:
                pass

        # HTML page
        if "text/html" in content_type:
            html = resp.text
            break

    # Populate from JSON if available
    if json_data:
        _populate_from_json(result, json_data)

    # Populate from HTML if JSON did not provide data
    if html and all(v in ("Not publicly available", []) for k, v in result.items()
                    if k not in ("username",)):
        _populate_from_html(result, html)

    return result


def _populate_from_json(result, data):
    """Map JSON fields into the result dict."""
    field_map = {
        "name": "name",
        "bio": "bio",
        "job": "job",
        "workplace": "workplace",
        "college": "college",
        "city": "city",
        "hometown": "hometown",
        "organizations": "organizations",
        "connections": "connections",
    }
    for key, src in field_map.items():
        val = data.get(src)
        if val:
            result[key] = val

    posts = data.get("posts")
    if isinstance(posts, list):
        result["posts"] = posts


def _populate_from_html(result, html):
    """Best-effort extraction of public fields from HTML."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return

    soup = BeautifulSoup(html, "html.parser")

    # Look for common meta tags or data attributes
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        result["bio"] = meta["content"]

    # Try to find profile fields by class/id patterns
    def _text(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else None

    name = _text(".profile-name, #profile-name, [class*='name']")
    if name:
        result["name"] = name

    bio = _text(".profile-bio, #profile-bio, [class*='bio']")
    if bio:
        result["bio"] = bio

    job = _text(".profile-job, #profile-job, [class*='job']")
    if job:
        result["job"] = job

    workplace = _text(".profile-workplace, #profile-workplace, [class*='workplace']")
    if workplace:
        result["workplace"] = workplace

    college = _text(".profile-college, #profile-college, [class*='college']")
    if college:
        result["college"] = college

    city = _text(".profile-city, #profile-city, [class*='city']")
    if city:
        result["city"] = city

    hometown = _text(".profile-hometown, #profile-hometown, [class*='hometown']")
    if hometown:
        result["hometown"] = hometown

    orgs = _text(".profile-organizations, #profile-organizations, [class*='organization']")
    if orgs:
        result["organizations"] = orgs

    conn = _text(".profile-connections, #profile-connections, [class*='connection']")
    if conn:
        result["connections"] = conn