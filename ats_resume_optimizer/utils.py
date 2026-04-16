"""Filename and path utilities."""

import re
from datetime import datetime
from pathlib import Path

from ats_resume_optimizer.config import OUTPUT_DIR


def sanitize_for_filename(text: str) -> str:
    """Return a filesystem-safe string (alphanumeric, underscore, hyphen only)."""
    return (
        "".join(c for c in text if c.isalnum() or c in ("_", "-")).strip("_-")
        or "file"
    )


def extract_name_from_html(content_html: str) -> str:
    """Extract the candidate name from the resume HTML <h1> tag."""
    match = re.search(r"<h1[^>]*>(.*?)</h1>", content_html, re.IGNORECASE | re.DOTALL)
    if match:
        name = re.sub(r"<[^>]+>", "", match.group(1)).strip()
        if name:
            return name
    return "Resume"


def build_output_path(candidate_name: str, company: str | None = None) -> Path:
    """Build output PDF path.

    With company:  Name_Company.pdf  (e.g. John_Doe_Google.pdf)
    Without:       Name_DDMMMYYYY.pdf (e.g. John_Doe_16APR2026.pdf)
    """
    name_clean = sanitize_for_filename(candidate_name.replace(" ", "_"))
    if company and company.strip():
        suffix = sanitize_for_filename(company.strip().replace(" ", "_"))
    else:
        suffix = datetime.now().strftime("%d%b%Y").upper()
    filename = f"{name_clean}_{suffix}.pdf"
    return OUTPUT_DIR / filename
