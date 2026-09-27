"""
main.py - Entry point for the Classroom OSINT Investigation Tool.

This is an authorized laboratory tool for investigating a fictional
Facebook clone. It only communicates through the normal HTTP/web
interface and only collects publicly exposed information.
"""

import sys

from config import TARGET_URL
from connection import check_connection
from profile import show_profile_menu


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
    print("  [2] Investigate Public Username")
    print("  [3] View Public Profile")
    print("  [4] Exit")
    print()


def test_connection():
    print("[+] Checking target...")
    reachable, status, reason = check_connection()

    if reachable:
        print("[+] Target is reachable")
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


def main():
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
            username = input("Enter fictional username: ").strip()
            if username:
                print("[+] Investigating username...")
                from username import investigate_username
                data = investigate_username(username)
                print(f"Name: {data['name']}")
                print(f"Username: {data['username']}")
                print(f"Bio: {data['bio']}")
            else:
                print("Username cannot be empty.")
        elif choice == "3":
            show_profile_menu()
        elif choice == "4":
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Invalid option. Please select 1-4.")

        input()


if __name__ == "__main__":
    main()