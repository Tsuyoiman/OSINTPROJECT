#!/usr/bin/env bash
# install.sh - Robust installer for the Classroom OSINT Investigation Tool
# on Kali Linux.
#
# Designed to work even when:
#   - python3 -m venv fails because ensurepip / python3.X-venv is missing
#   - apt's package index is stale or a third-party repo (e.g. WineHQ) has
#     a broken/expired signing key that blocks "apt update"
#   - Kali's system Python is "externally managed" (PEP 668) and refuses
#     a plain "pip install"
#
# Strategy: try a virtualenv first; if that fails for any reason, fall
# back to installing dependencies straight into the system interpreter
# with --break-system-packages, which is the supported Kali workaround
# for small standalone tools like this one.

set -uo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "[*] Classroom OSINT Investigation Tool - installer"
echo "[*] Project directory: $DIR"
echo

# --- Optional system tools used by the lab (best-effort, never fatal) ---
if command -v apt-get >/dev/null 2>&1; then
    echo "[*] Refreshing package index (best-effort, ignoring unrelated repo errors)..."
    sudo apt-get update -y 2>&1 | tail -n 5 || true

    echo "[*] Installing optional lab tools if missing: nmap, exiftool..."
    sudo apt-get install -y --no-install-recommends nmap libimage-exiftool-perl 2>&1 | tail -n 10 || true
fi

# --- Python dependency installation ---
INSTALLED=0

if command -v python3 >/dev/null 2>&1; then
    echo "[*] Attempting to create an isolated virtual environment (.venv)..."
    rm -rf .venv
    if python3 -m venv .venv 2>/tmp/osint_venv_err.log; then
        echo "[+] Virtual environment created."
        # shellcheck disable=SC1091
        source .venv/bin/activate
        if python -m pip install --upgrade pip -q && python -m pip install -q -r requirements.txt; then
            echo "[+] Dependencies installed inside .venv"
            INSTALLED=1
        else
            echo "[-] pip install inside .venv failed, will fall back to system Python."
        fi
        deactivate 2>/dev/null || true
    else
        echo "[-] Could not create a virtual environment on this system:"
        sed 's/^/    /' /tmp/osint_venv_err.log 2>/dev/null || true
        echo "    (commonly caused by a missing python3-venv/ensurepip package)"
        rm -rf .venv
    fi
fi

if [ "$INSTALLED" -eq 0 ]; then
    echo "[*] Falling back to installing dependencies for the system Python3..."
    if python3 -m pip install -r requirements.txt 2>/tmp/osint_pip_err.log; then
        INSTALLED=1
    elif python3 -m pip install --break-system-packages -r requirements.txt 2>>/tmp/osint_pip_err.log; then
        echo "[+] Installed with --break-system-packages (Kali's externally-managed Python)."
        INSTALLED=1
    else
        echo "[-] pip install failed. Last error:"
        tail -n 20 /tmp/osint_pip_err.log 2>/dev/null || true
        echo
        echo "[-] Manual fallback: try one of the following yourself, then re-run:"
        echo "      sudo apt install -y python3-requests"
        echo "      python3 -m pip install --break-system-packages -r requirements.txt"
    fi
fi

chmod +x osint-lab 2>/dev/null || true

echo
if [ "$INSTALLED" -eq 1 ]; then
    echo "======================================================"
    echo "[+] Installation complete."
    echo "[+] Run the tool with:  ./osint-lab"
    echo "    (or: python3 main.py)"
    echo "======================================================"
else
    echo "======================================================"
    echo "[-] Automatic installation did not fully succeed."
    echo "    See the messages above for the exact error, then"
    echo "    retry the manual fallback commands shown above."
    echo "======================================================"
    exit 1
fi
