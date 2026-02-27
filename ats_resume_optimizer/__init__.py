"""ATS Resume Optimizer: tailor resumes to job descriptions for better ATS match."""

from pathlib import Path

from ats_resume_optimizer.agent import export_resume_pdf, optimize_resume, run_resume_agent
from ats_resume_optimizer.config import BASE_DIR, OUTPUT_DIR, RESUME_DIR

__version__ = (Path(__file__).resolve().parent.parent / "VERSION").read_text().strip()

__all__ = [
    "__version__",
    "export_resume_pdf",
    "optimize_resume",
    "run_resume_agent",
    "BASE_DIR",
    "RESUME_DIR",
    "OUTPUT_DIR",
]
