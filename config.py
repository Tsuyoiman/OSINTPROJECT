"""
config.py - Central configuration for the Classroom OSINT Investigation Tool.

Edit LAB_IP / LAB_PORT to match the instructor-assigned Facebook clone
instance for your classroom session.
"""

# Address of the authorized fictional Facebook-clone lab target.
LAB_IP = "192.168.100.7"
LAB_PORT = 8000
FRONTEND_PORT = 3000

TARGET_URL = f"http://{LAB_IP}:{LAB_PORT}"
FRONTEND_URL = f"http://{LAB_IP}:{FRONTEND_PORT}"

# The only network range students are authorized to investigate/scan in
# this laboratory. Used to guard the network-recon feature so it can never
# be pointed at an out-of-scope host by accident.
AUTHORIZED_NETWORK = "192.168.100.0/24"

# Where downloaded evidence (images) and generated reports are written.
OUTPUT_DIR = "output"
IMAGES_DIR = "output/images"