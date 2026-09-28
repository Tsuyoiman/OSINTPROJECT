"""
main.py - Entry point for the Classroom OSINT Investigation Tool.

This is an authorized laboratory tool for investigating a fictional
Facebook clone. It only communicates through the normal HTTP/web
interface and only collects publicly exposed information from the
authorized classroom network (see config.AUTHORIZED_NETWORK).

Investigation workflow:
  1. Test Target Connection
  2. Search Public Users (by name/keyword clue)
  3. Investigate Username / View Full Public Profile
  4. Correlate Friends & Organizations (pivot to related profiles)
  5. Download Profile Images (for ExifTool analysis)
  6. Authorized Network Reconnaissance (Nmap, classroom subnet only)
  7. Generate OSINT Investigation Report
  8. Exit
"""

import sys

from config import TARGET_URL
from connection import check_connection


def print_header():
    print()
    print("=" * 50)
    print("CLASSROOM OSINT INVESTIGATION TOOL")
    print("=" * 50)
    print(f"Target: {TARGET_URL}")
    print()


def print_menu():
    print("Menu:")
    print("  [1] Test Target Connection")
    print("  [2] Search Public Users (first name, last name, or both)")
    print("  [3] Investigate Profile (username or registration email)")
    print("  [4] Correlate Friends & Organizations")
    print("  [5] Download Profile Images (for ExifTool)")
    print("  [6] Authorized Network Reconnaissance (Nmap)")
    print("  [7] Generate OSINT Investigation Report")
    print("  [8] Exit")
    print()


def test_connection():
    print("[+] Checking target...")
    reachable, status, reason = check_connection()

    if reachable:
        print(f"[+] Target is reachable (HTTP {status})")
        print("[+] Classroom website detected")
    else:
        print("[-] Target unavailable")
        print("Possible causes:")
        print("  * Facebook clone is not running")
        print("  * Incorrect IP")
        print("  * Incorrect port")
        print("  * Windows firewall")
        print("  * VMware networking problem")
        if reason:
            print(f"  Details: {reason}")


def search_users_menu():
    from username import search_users

    query = input("Enter first name, last name, full name, or email: ").strip()
    if not query:
        print("Search query cannot be empty.")
        return

    print("[+] Searching public users...")
    results = search_users(query)
    if not results:
        print("[-] No public matches found.")
        return

    print(f"[+] {len(results)} match(es) found:")
    for r in results:
        name = f"{r.get('first_name', '')} {r.get('last_name', '')}".strip()
        print(f"  - {name} (@{r.get('username')})")
    print("Use option 3 with a displayed username or the registration email.")


def investigate_profile_menu(state):
    from profile import show_profile_menu

    data = show_profile_menu()
    if data and data.get("found"):
        state["last_profile"] = data
        state["primary_username"] = data["username"]


def profile_for_action(state, action):
    """Return a profile selected for a correlation or image action."""
    from profile import render_profile
    from username import investigate_username

    previous = state.get("last_profile")
    prompt = (
        f"Enter username, full name, or registration email for {action} "
        "(press Enter to use the last profile): "
    )
    identifier = input(prompt).strip()
    if not identifier:
        if previous:
            return previous
        print("[-] No profile selected. Enter a username, name, or email.")
        return None

    data = investigate_username(identifier)
    render_profile(data)
    if not data.get("found"):
        return None

    state["last_profile"] = data
    state["primary_username"] = data["username"]
    return data


def correlate_menu(state):
    from connections import find_related_profiles

    profile = profile_for_action(state, "correlation")
    if not profile:
        return

    print(f"[+] Exploring public friends of @{profile['username']}...")
    related = find_related_profiles(profile)
    if not related:
        print("[-] No public friends to correlate.")
        return

    from evidence import add_entry

    print(f"[+] {len(related)} related profile(s) found:")
    for r in related:
        shared = ", ".join(r["shared_organizations"]) or "none"
        print(f"  - {r['name']} (@{r['username']}) | Workplace: {r['workplace']} | Shared orgs: {shared}")

    add_entry(
        "correlation",
        f"Correlated {len(related)} friend(s) of @{profile['username']}",
        details=[
            f"{r['name']} (@{r['username']}) shared orgs: {', '.join(r['shared_organizations']) or 'none'}"
            for r in related
        ],
    )


def download_images_menu(state):
    from images import download_profile_images, run_exiftool
    from evidence import add_entry

    profile = profile_for_action(state, "image download")
    if not profile:
        return

    saved = download_profile_images(profile)
    if not saved:
        print("[-] No public images available to download.")
        return

    for path in saved:
        print(f"[+] Running ExifTool on {path} ...")
        run_exiftool(path)

    add_entry("image", f"Downloaded {len(saved)} image(s) for @{profile['username']}", details=saved)


def recon_menu():
    from recon import run_recon
    from config import LAB_IP
    from evidence import add_entry

    target = input(f"Target IP to scan [{LAB_IP}]: ").strip() or LAB_IP
    output = run_recon(target)
    if output:
        add_entry("recon", f"Nmap scan of {target}", details=output[:2000])


def generate_report_menu(state):
    from report import save_report

    save_report(primary_username=state.get("primary_username"))


def main():
    state = {"last_profile": None, "primary_username": None}

    while True:
        print_header()
        print_menu()

        try:
            choice = input("Select an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("Goodbye.")
            sys.exit(0)

        if choice == "1":
            test_connection()
        elif choice == "2":
            search_users_menu()
        elif choice == "3":
            investigate_profile_menu(state)
        elif choice == "4":
            correlate_menu(state)
        elif choice == "5":
            download_images_menu(state)
        elif choice == "6":
            recon_menu()
        elif choice == "7":
            generate_report_menu(state)
        elif choice == "8":
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Invalid option. Please select 1-8.")

        input()


if __name__ == "__main__":
    main()