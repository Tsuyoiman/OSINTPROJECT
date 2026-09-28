"""
images.py - Downloads a profile's publicly exposed images so students can
analyze them with ExifTool.

This only fetches images already served publicly by the classroom website;
it does not access storage or the database directly.
"""

import os
import shutil
import subprocess

import requests

from config import FRONTEND_URL, TARGET_URL, IMAGES_DIR


def _resolve_image_url(path):
    """Turn a profile's picture/cover path into a fetchable absolute URL."""
    if not path:
        return None
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    # The Express API returns relative image paths, but the React frontend
    # normally serves the files from its public directory.
    return f"{FRONTEND_URL}{path}"


def download_profile_images(profile):
    """
    Download the profile picture and cover photo (if publicly set) to
    output/images/<username>/. Returns a list of saved file paths.
    """
    username = profile.get("username", "unknown")
    target_dir = os.path.join(IMAGES_DIR, username)
    os.makedirs(target_dir, exist_ok=True)

    saved = []
    for label, path in (("picture", profile.get("picture")), ("cover", profile.get("cover"))):
        url = _resolve_image_url(path)
        if not url:
            continue
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 404:
                api_url = _resolve_api_image_url(path)
                resp = requests.get(api_url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"[-] Could not download {label}: {e}")
            continue
        if resp.status_code != 200:
            print(f"[-] {label} not available (HTTP {resp.status_code})")
            continue

        ext = os.path.splitext(path)[1] or ".jpg"
        filename = os.path.join(target_dir, f"{label}{ext}")
        with open(filename, "wb") as f:
            f.write(resp.content)
        saved.append(filename)
        print(f"[+] Saved {label}: {filename}")

    return saved


def _resolve_api_image_url(path):
    """Return the API-host fallback for deployments serving assets there."""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = "/" + path
    return f"{TARGET_URL}{path}"


def run_exiftool(filepath):
    """
    Run ExifTool on a downloaded image if it is installed, and return its
    text output. Prints instructions instead if ExifTool is not present.
    """
    if shutil.which("exiftool") is None:
        print("[-] exiftool is not installed.")
        print("    Install it on Kali with: sudo apt install -y libimage-exiftool-perl")
        return None

    try:
        result = subprocess.run(
            ["exiftool", filepath], capture_output=True, text=True, timeout=15
        )
        print(result.stdout)
        return result.stdout
    except Exception as e:
        print(f"[-] Failed to run exiftool: {e}")
        return None
