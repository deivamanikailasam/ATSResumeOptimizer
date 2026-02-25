"""Paths and directory configuration for the ATS Resume Optimizer."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESUME_DIR = BASE_DIR / "memory" / "docs"
OUTPUT_DIR = RESUME_DIR / "generated"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
