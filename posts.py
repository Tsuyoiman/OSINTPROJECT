"""
posts.py - Formats the public posts already included in a profile lookup.

The backend does not expose a separate "/api/posts" endpoint; public posts
for a profile are returned inline by GET /publicProfile/<username> (subject
to that user's privacy settings). This module just renders them.
"""


def format_posts(profile):
    """Return a list of printable post strings from an investigated profile."""
    lines = []
    for i, post in enumerate(profile.get("posts") or [], 1):
        if isinstance(post, str):
            text = post
        else:
            text = post.get("text") or "(no text - image/background post)"
        lines.append(f"{i}. {text}")
    return lines