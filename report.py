"""
report.py - Generates a simple text report from investigation results.
"""

import os
from datetime import datetime


def save_report(data, output_dir="output"):
    """Save an investigation report to a text file."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(output_dir, f"report_{data['username']}_{timestamp}.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("CLASSROOM OSINT INVESTIGATION REPORT\n")
        f.write("=" * 40 + "\n")
        f.write(f"Username:    {data['username']}\n")
        f.write(f"Name:        {data['name']}\n")
        f.write(f"Bio:         {data['bio']}\n")
        f.write(f"Job:         {data['job']}\n")
        f.write(f"Workplace:   {data['workplace']}\n")
        f.write(f"College:     {data['college']}\n")
        f.write(f"City:        {data['city']}\n")
        f.write(f"Hometown:    {data['hometown']}\n")
        f.write(f"Orgs:        {data['organizations']}\n")
        f.write(f"Connections: {data['connections']}\n")
        f.write("-" * 40 + "\n")
        f.write("Public Posts:\n")
        if data["posts"]:
            for i, post in enumerate(data["posts"], 1):
                text = post if isinstance(post, str) else post.get("text", str(post))
                f.write(f"  {i}. {text}\n")
        else:
            f.write("  Not publicly available\n")
        f.write("=" * 40 + "\n")

    print(f"[+] Report saved to: {filename}")
    return filename