"""
profile.py - Renders the public profile investigation results and logs
the finding as evidence for the final OSINT report.
"""

from username import investigate_username
from evidence import add_entry


def show_profile_menu():
    """Prompt for a username and display whatever the website exposes."""
    username = input("Enter fictional username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return None

    print("[+] Retrieving public profile...")
    data = investigate_username(username)
    render_profile(data)
    return data


def render_profile(data):
    """Print a profile dict and log it as evidence."""
    print()
    print("=" * 50)
    print("PUBLIC PROFILE")
    print("=" * 50)

    if not data.get("found"):
        print(f"[-] No public profile found for '{data['username']}'.")
        print("    Try the exact username handle (e.g. 'megan_fox') or use")
        print("    option 2 to search by name/keyword first.")
        print("=" * 50)
        return

    print(f"Name:            {data['name']}")
    print(f"Username:        {data['username']}")
    print(f"Bio:             {data['bio']}")
    print(f"Job:             {data['job']}")
    print(f"Workplace:       {data['workplace']}")
    print(f"College:         {data['college']}")
    print(f"Current City:    {data['city']}")
    print(f"Hometown:        {data['hometown']}")
    print(f"Organizations:   {data['organizations']}")
    print(f"Connections:     {data['connections']}")
    if data.get("clues"):
        print(f"Clues/Leads:     {', '.join(data['clues'])}")
    print("-" * 50)
    print("Public Posts:")
    if data["posts"]:
        for i, post in enumerate(data["posts"], 1):
            text = post if isinstance(post, str) else post.get("text", str(post))
            print(f"  {i}. {text}")
    else:
        print("  Not publicly available")
    if data.get("friends"):
        print("-" * 50)
        print("Public Friends (correlation leads):")
        for friend in data["friends"]:
            fname = f"{friend.get('first_name', '')} {friend.get('last_name', '')}".strip()
            print(f"  - {fname} (@{friend.get('username')})")
    print("=" * 50)

    add_entry(
        "profile",
        f"{data['name']} (@{data['username']})",
        details={
            "bio": data["bio"],
            "job": data["job"],
            "workplace": data["workplace"],
            "college": data["college"],
            "city": data["city"],
            "hometown": data["hometown"],
            "organizations_list": data.get("organizations_list", []),
            "clues": data.get("clues", []),
            "posts": data.get("posts", []),
            "friends": [f.get("username") for f in data.get("friends", [])],
        },
    )