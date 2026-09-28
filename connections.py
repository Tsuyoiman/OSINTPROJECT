"""
connections.py - Correlation step: explore the friends/organizations of an
already-discovered profile to find related targets.

The backend does not expose a separate "/connections" endpoint; public
friends are already included in GET /publicProfile/<username>. This module
pivots from one profile's public friends and shared organizations into new
investigation leads, which is the core "correlation" concept of the lab.
"""

from username import investigate_username


def find_related_profiles(profile):
    """
    Given an already-fetched profile dict (from investigate_username),
    pivot into each public friend's profile and flag any shared
    organizations. Returns a list of dicts:
      {"username", "name", "workplace", "shared_organizations": [...]}
    """
    related = []
    own_orgs = set(profile.get("organizations_list") or [])

    for friend in profile.get("friends") or []:
        friend_username = friend.get("username")
        if not friend_username:
            continue

        friend_profile = investigate_username(friend_username)
        friend_orgs = set(friend_profile.get("organizations_list") or [])
        shared = sorted(own_orgs & friend_orgs)

        related.append(
            {
                "username": friend_username,
                "name": friend_profile.get("name", "Not publicly available"),
                "workplace": friend_profile.get("workplace", "Not publicly available"),
                "shared_organizations": shared,
            }
        )

    return related