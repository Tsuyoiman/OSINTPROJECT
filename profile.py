"""
profile.py - Renders the public profile investigation results.
"""

from username import investigate_username


def show_profile_menu():
    """Prompt for a username and display whatever the website exposes."""
    username = input("Enter fictional username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return

    print("[+] Retrieving public profile...")
    data = investigate_username(username)

    print()
    print("=" * 50)
    print("PUBLIC PROFILE")
    print("=" * 50)
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
    print("-" * 50)
    print("Public Posts:")
    if data["posts"]:
        for i, post in enumerate(data["posts"], 1):
            text = post if isinstance(post, str) else post.get("text", str(post))
            print(f"  {i}. {text}")
    else:
        print("  Not publicly available")
    print("=" * 50)