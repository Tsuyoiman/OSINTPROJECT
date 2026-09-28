"""
report.py - Generates a structured OSINT investigation report from the
evidence log collected during the session (evidence.py), following the
17-section classroom report template.
"""

import os
from datetime import datetime

from config import TARGET_URL, AUTHORIZED_NETWORK, OUTPUT_DIR
from evidence import get_log


SECTIONS = [
    "1. Investigation Objective",
    "2. Target Identification",
    "3. Scope",
    "4. Public Information Discovered",
    "5. Username/Profile Findings",
    "6. Public Posts",
    "7. Related Users",
    "8. Organizations/Projects",
    "9. Events",
    "10. Image/Metadata Findings",
    "11. Network Reconnaissance Findings",
    "12. Evidence",
    "13. Relationship/Correlation Analysis",
    "14. Security Observations",
    "15. Limitations",
    "16. Ethical Considerations",
    "17. Conclusion",
]


def _entries(log, category):
    return [e for e in log if e["category"] == category]


def _format_details(details, indent="    "):
    lines = []
    if isinstance(details, dict):
        for k, v in details.items():
            lines.append(f"{indent}{k}: {v}")
    elif isinstance(details, list):
        for item in details:
            lines.append(f"{indent}- {item}")
    elif details:
        lines.append(f"{indent}{details}")
    return lines


def save_report(primary_username=None, output_dir=OUTPUT_DIR):
    """
    Build and save the full OSINT report from everything collected in the
    evidence log this session (profiles viewed, correlations explored,
    images downloaded, recon performed).
    """
    os.makedirs(output_dir, exist_ok=True)
    log = get_log()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    label = primary_username or (log[0]["summary"] if log else "session")
    safe_label = "".join(c for c in str(label) if c.isalnum() or c in ("_", "-")) or "session"
    filename = os.path.join(output_dir, f"report_{safe_label}_{timestamp}.txt")

    profile_entries = _entries(log, "profile")
    correlation_entries = _entries(log, "correlation")
    image_entries = _entries(log, "image")
    recon_entries = _entries(log, "recon")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("CLASSROOM OSINT INVESTIGATION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        f.write(SECTIONS[0] + "\n")
        f.write(
            "Demonstrate a controlled, ethical OSINT investigation of a\n"
            "fictional social-media environment, correlating multiple public\n"
            "clues into related findings.\n\n"
        )

        f.write(SECTIONS[1] + "\n")
        f.write(f"Target website: {TARGET_URL}\n")
        f.write(f"Primary username investigated: {label}\n\n")

        f.write(SECTIONS[2] + "\n")
        f.write(f"Authorized network: {AUTHORIZED_NETWORK}\n")
        f.write("Only publicly exposed data from the authorized classroom\n")
        f.write("Facebook clone was accessed. No authentication bypass, no\n")
        f.write("direct database access, and no real individuals were involved.\n\n")

        f.write(SECTIONS[3] + "\n")
        if not log:
            f.write("No evidence collected yet.\n\n")
        else:
            for e in log:
                f.write(f"[{e['timestamp']}] ({e['category']}) {e['summary']}\n")
            f.write("\n")

        f.write(SECTIONS[4] + "\n")
        if not profile_entries:
            f.write("No profiles investigated.\n\n")
        else:
            for e in profile_entries:
                f.write(f"- {e['summary']}\n")
                f.writelines(l + "\n" for l in _format_details(e["details"]))
            f.write("\n")

        f.write(SECTIONS[5] + "\n")
        for e in profile_entries:
            posts = (e["details"] or {}).get("posts") if isinstance(e["details"], dict) else None
            if posts:
                f.write(f"Posts for {e['summary']}:\n")
                for i, post in enumerate(posts, 1):
                    text = post if isinstance(post, str) else post.get("text", str(post))
                    f.write(f"  {i}. {text}\n")
        if not any(
            isinstance(e["details"], dict) and e["details"].get("posts") for e in profile_entries
        ):
            f.write("No public posts discovered.\n")
        f.write("\n")

        f.write(SECTIONS[6] + "\n")
        if not correlation_entries:
            f.write("No correlation step performed.\n\n")
        else:
            for e in correlation_entries:
                f.write(f"- {e['summary']}\n")
                f.writelines(l + "\n" for l in _format_details(e["details"]))
            f.write("\n")

        f.write(SECTIONS[7] + "\n")
        orgs = set()
        for e in profile_entries:
            d = e["details"] or {}
            if isinstance(d, dict):
                for o in d.get("organizations_list") or []:
                    orgs.add(o)
        if orgs:
            for o in sorted(orgs):
                f.write(f"- {o}\n")
        else:
            f.write("No organizations/projects discovered.\n")
        f.write("\n")

        f.write(SECTIONS[8] + "\n")
        clues = set()
        for e in profile_entries:
            d = e["details"] or {}
            if isinstance(d, dict):
                for c in d.get("clues") or []:
                    clues.add(c)
        if clues:
            f.write("Fictional clue references discovered (used as event/project leads):\n")
            for c in sorted(clues):
                f.write(f"- {c}\n")
        else:
            f.write("No event references discovered.\n")
        f.write("\n")

        f.write(SECTIONS[9] + "\n")
        if not image_entries:
            f.write("No images downloaded/analyzed.\n\n")
        else:
            for e in image_entries:
                f.write(f"- {e['summary']}\n")
                f.writelines(l + "\n" for l in _format_details(e["details"]))
            f.write("\n")

        f.write(SECTIONS[10] + "\n")
        if not recon_entries:
            f.write("No network reconnaissance performed.\n\n")
        else:
            for e in recon_entries:
                f.write(f"- {e['summary']}\n")
                f.writelines(l + "\n" for l in _format_details(e["details"]))
            f.write("\n")

        f.write(SECTIONS[11] + "\n")
        f.write(f"Total evidence entries collected: {len(log)}\n\n")

        f.write(SECTIONS[12] + "\n")
        f.write(
            "Public profile fields, friends lists, organizations, clues,\n"
            "posts, and images were cross-referenced to identify\n"
            "relationships between fictional accounts.\n\n"
        )

        f.write(SECTIONS[13] + "\n")
        f.write(
            "Note any fields the fictional accounts unintentionally expose\n"
            "(e.g. workplace, hometown, organizations) that, combined, allow\n"
            "identification of real-world-style patterns.\n\n"
        )

        f.write(SECTIONS[14] + "\n")
        f.write(
            "This report only reflects data available through this session.\n"
            "Locked profiles, friends-only posts, and private data are\n"
            "intentionally excluded.\n\n"
        )

        f.write(SECTIONS[15] + "\n")
        f.write(
            "All data belongs to fictional classroom accounts. No real\n"
            "individuals, credentials, or systems were targeted. All\n"
            "investigation stayed within the authorized network and used\n"
            "only public interfaces.\n\n"
        )

        f.write(SECTIONS[16] + "\n")
        f.write(
            "Individually harmless public information became more\n"
            "informative once correlated: usernames led to profiles, which\n"
            "led to organizations, clues, related people, and images -\n"
            "demonstrating why organizations should limit public exposure.\n"
        )

    print(f"[+] Report saved to: {filename}")
    return filename