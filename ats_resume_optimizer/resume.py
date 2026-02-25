"""Resume PDF text extraction."""

from pathlib import Path

from pypdf import PdfReader


def extract_resume_text(pdf_path: Path) -> str:
    """Extract text from a resume PDF. Raises ValueError if no text is found."""
    reader = PdfReader(str(pdf_path))
    pages_text = [page.extract_text() or "" for page in reader.pages]
    resume_text = "\n".join(pages_text).strip()
    if not resume_text:
        raise ValueError(
            "No text extracted from resume PDF (is it scanned/only images?)."
        )
    return resume_text
