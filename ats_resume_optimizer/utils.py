"""Filename and path utilities."""

from pathlib import Path

from ats_resume_optimizer.config import OUTPUT_DIR


def sanitize_for_filename(text: str) -> str:
    """Return a filesystem-safe string (alphanumeric, underscore, hyphen only)."""
    return (
        "".join(c for c in text if c.isalnum() or c in ("_", "-")).strip("_-")
        or "file"
    )


def build_output_path(job_title: str, company: str) -> Path:
    """Build output PDF path from job title and company."""
    title_clean = sanitize_for_filename(job_title.replace(" ", "_"))
    company_clean = sanitize_for_filename(company.replace(" ", "_"))
    filename = f"{title_clean}_{company_clean}.pdf"
    return OUTPUT_DIR / filename
