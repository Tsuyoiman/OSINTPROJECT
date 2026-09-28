"""
recon.py - Authorized network reconnaissance step (Nmap wrapper).

Safety rule: this module refuses to scan any address outside the
classroom's authorized network range (config.AUTHORIZED_NETWORK). This
laboratory teaches authorized reconnaissance only.
"""

import ipaddress
import shutil
import subprocess

from config import AUTHORIZED_NETWORK, LAB_IP


def is_authorized_target(ip_str):
    """Return True only if ip_str falls inside AUTHORIZED_NETWORK."""
    try:
        ip = ipaddress.ip_address(ip_str)
        network = ipaddress.ip_network(AUTHORIZED_NETWORK, strict=False)
    except ValueError:
        return False
    return ip in network


def run_recon(target_ip=None):
    """
    Run a basic authorized Nmap service scan against target_ip (defaults
    to the configured LAB_IP). Refuses anything outside
    config.AUTHORIZED_NETWORK. Returns the scan output text, or None.
    """
    target_ip = (target_ip or LAB_IP).strip()

    if not is_authorized_target(target_ip):
        print(f"[-] Refusing to scan {target_ip}: outside authorized network {AUTHORIZED_NETWORK}")
        print("    This laboratory only permits scanning the classroom network.")
        return None

    if shutil.which("nmap") is None:
        print("[-] nmap is not installed.")
        print("    Install it on Kali with: sudo apt install -y nmap")
        return None

    print(f"[+] Running authorized service scan against {target_ip} ...")
    try:
        result = subprocess.run(
            ["nmap", "-sV", "-Pn", target_ip],
            capture_output=True,
            text=True,
            timeout=120,
        )
        print(result.stdout)
        return result.stdout
    except subprocess.TimeoutExpired:
        print("[-] Nmap scan timed out.")
        return None
    except Exception as e:
        print(f"[-] Failed to run nmap: {e}")
        return None
