"""
evidence.py - In-memory evidence log for the current investigation session.

Every module that discovers something (a profile, a correlation, a
downloaded image, a recon result) calls add_entry() so that the final
report (report.py) can assemble a single, structured document that
mirrors the OSINT investigation chain instead of one isolated lookup.
"""

from datetime import datetime

# Session-scoped list of evidence entries. Cleared only when the program
# restarts, so a full investigation (search -> profile -> correlate ->
# image -> recon -> report) can be documented in one report.
_LOG = []


def add_entry(category, summary, details=None):
    """
    Record one piece of evidence.

    category: short label, e.g. "profile", "correlation", "image", "recon"
    summary:  one-line human-readable description
    details:  optional dict/list/str with the full data for the report
    """
    _LOG.append(
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "summary": summary,
            "details": details,
        }
    )


def get_log():
    """Return the full evidence log collected so far."""
    return list(_LOG)


def clear_log():
    """Reset the evidence log (used between separate investigations)."""
    _LOG.clear()
