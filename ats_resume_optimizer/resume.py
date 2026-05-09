"""Resume PDF text extraction and structural analysis."""

import re
from pathlib import Path

from pypdf import PdfReader

_KNOWN_SECTION_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("summary", re.compile(
        r"^(professional\s+summary|summary|profile|objective|"
        r"career\s+summary|executive\s+summary|about\s*me)",
        re.IGNORECASE,
    )),
    ("skills", re.compile(
        r"^(technical\s+skills|skills|core\s+competencies|"
        r"competencies|areas?\s+of\s+expertise|technologies|"
        r"proficiencies|tools\s*(?:&|and)?\s*technologies|"
        r"programming\s+languages|languages?\s*(?:&|and|/)\s*"
        r"(?:frameworks|libraries|tools|technologies)|"
        r"frameworks\s*(?:&|and|/)\s*(?:libraries|tools|technologies)|"
        r"libraries\s*(?:&|and|/)\s*(?:frameworks|tools|technologies)|"
        r"developer\s+tools|devops\s*(?:&|and|/)?\s*tools|"
        r"cloud\s*(?:&|and|/)\s*(?:devops|platforms|tools)|"
        r"databases?|methodologies)",
        re.IGNORECASE,
    )),
    ("experience", re.compile(
        r"^(professional\s+experience|experience|work\s+experience|"
        r"employment\s*history|career\s+history|work\s+history|"
        r"relevant\s+experience)",
        re.IGNORECASE,
    )),
    ("education", re.compile(
        r"^(education|academic\s+background|academic\s+qualifications|"
        r"degrees)",
        re.IGNORECASE,
    )),
    ("projects", re.compile(
        r"^(projects|notable\s+projects|key\s+projects|"
        r"personal\s+projects|selected\s+projects|side\s+projects)",
        re.IGNORECASE,
    )),
    ("certifications", re.compile(
        r"^(certifications?|licenses?\s*(?:&|and)?\s*certifications?|"
        r"professional\s+certifications?|credentials)",
        re.IGNORECASE,
    )),
    ("publications", re.compile(
        r"^(publications?|research\s+publications?|papers|"
        r"selected\s+publications?)",
        re.IGNORECASE,
    )),
    ("awards", re.compile(
        r"^(awards?\s*(?:&|and)?\s*honors?|honors?\s*(?:&|and)?\s*awards?|"
        r"recognition|achievements|distinctions)",
        re.IGNORECASE,
    )),
    ("volunteer", re.compile(
        r"^(volunteer\s*(?:experience|work)?|community\s+(?:service|involvement)|"
        r"civic\s+engagement)",
        re.IGNORECASE,
    )),
    ("languages", re.compile(
        r"^(languages?|language\s+proficiency|linguistic\s+skills)",
        re.IGNORECASE,
    )),
    ("affiliations", re.compile(
        r"^(professional\s+affiliations?|affiliations?|memberships?|"
        r"professional\s+memberships?|organizations?)",
        re.IGNORECASE,
    )),
    ("patents", re.compile(
        r"^(patents?|intellectual\s+property)",
        re.IGNORECASE,
    )),
    ("research", re.compile(
        r"^(research|research\s+experience|research\s+interests?)",
        re.IGNORECASE,
    )),
    ("teaching", re.compile(
        r"^(teaching\s*(?:experience)?|instruction|courses?\s+taught)",
        re.IGNORECASE,
    )),
    ("references", re.compile(
        r"^(references?|professional\s+references?)",
        re.IGNORECASE,
    )),
    ("interests", re.compile(
        r"^(interests?|hobbies?\s*(?:&|and)?\s*interests?|"
        r"personal\s+interests?)",
        re.IGNORECASE,
    )),
    ("leadership", re.compile(
        r"^(leadership\s*(?:experience)?|leadership\s*(?:&|and)?\s*activities)",
        re.IGNORECASE,
    )),
    ("training", re.compile(
        r"^(training|professional\s+development|"
        r"continuing\s+education|workshops?)",
        re.IGNORECASE,
    )),
]


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


def _classify_heading(line: str) -> tuple[str, str]:
    """Return (section_id, original_heading) for a line that looks like a heading."""
    cleaned = line.strip().rstrip(":").strip()
    for section_id, pattern in _KNOWN_SECTION_PATTERNS:
        if pattern.match(cleaned):
            return section_id, cleaned
    return cleaned.lower().replace(" ", "_"), cleaned


def _looks_like_heading(line: str) -> bool:
    """Heuristic: identify lines that are likely resume section headings."""
    stripped = line.strip()
    if not stripped or len(stripped) > 50:
        return False
    if stripped.endswith((".", ",", ";")) and not stripped.endswith("..."):
        return False
    # Reject lines that look like skill lists or role descriptions
    if "," in stripped and stripped.count(",") >= 2:
        return False
    if re.search(r"\b(?:at|@)\b", stripped, re.IGNORECASE):
        return False
    # Known section heading patterns get highest priority — check BEFORE
    # the name filter since "Professional Summary" etc. are two words
    for _, pattern in _KNOWN_SECTION_PATTERNS:
        if pattern.match(stripped.rstrip(":")):
            return True
    # Two short capitalized words are likely a person's name, not a heading
    if re.match(r"^[A-Z][a-z]+ [A-Z][a-z]+$", stripped):
        return False
    # ALL-CAPS lines that are short (typical for resume headings)
    if re.match(r"^[A-Z][A-Z\s&/()-]+$", stripped) and len(stripped) <= 35:
        return True
    return False


def _count_bullets_in_block(lines: list[str]) -> int:
    """Count bullet-like lines (starting with -, *, bullet char, or digit.)."""
    count = 0
    for line in lines:
        stripped = line.strip()
        if re.match(r"^[-*•●◦▸▹►]", stripped) or re.match(r"^\d+\.", stripped):
            count += 1
    return count


def _finalize_section(section: dict, block: list[str]) -> None:
    """Compute bullet_count and has_items for a section from its content block."""
    bullet_count = _count_bullets_in_block(block)
    section["bullet_count"] = bullet_count
    section["has_items"] = bullet_count > 0 or len(block) > 2


def _extract_sections(lines: list[str]) -> tuple[list[dict], list[str]]:
    """Walk lines and split into sections. Returns (sections, last_block)."""
    sections: list[dict] = []
    current_section: dict | None = None
    current_block: list[str] = []

    for line in lines:
        if _looks_like_heading(line):
            if current_section is not None:
                _finalize_section(current_section, current_block)
                sections.append(current_section)
            section_id, heading = _classify_heading(line)
            current_section = {"id": section_id, "heading": heading}
            current_block = []
        else:
            current_block.append(line)

    if current_section is not None:
        _finalize_section(current_section, current_block)
        sections.append(current_section)

    return sections, current_block


def _extract_role_bullets(block: list[str]) -> list[dict]:
    """Parse an experience block into per-role bullet counts."""
    role_bullets: list[int] = []
    current_bullets = 0
    in_role = False

    for line in block:
        stripped = line.strip()
        is_bullet = bool(re.match(r"^[-*•●]", stripped))
        is_role_header = (
            stripped
            and not stripped.startswith(("-", "*", "•"))
            and len(stripped) < 80
        )

        if is_role_header:
            if in_role and current_bullets > 0:
                role_bullets.append(current_bullets)
            current_bullets = 0
            in_role = True
        elif is_bullet:
            current_bullets += 1

    if in_role and current_bullets > 0:
        role_bullets.append(current_bullets)

    return [
        {"role_index": idx, "bullet_count": count}
        for idx, count in enumerate(role_bullets)
    ]


def analyze_resume_structure(resume_text: str) -> dict:
    """Analyze the structural layout of a resume: sections, bullet counts, roles.

    Returns a dict with:
    - sections: list of {id, heading, bullet_count, has_items}
    - experience_roles: list of approximate role entries with bullet counts
    - total_sections: int
    - extra_sections: list of section ids beyond the standard 6
    """
    lines = resume_text.split("\n")
    sections, last_block = _extract_sections(lines)

    standard_ids = {
        "summary", "skills", "experience", "education",
        "projects", "certifications",
    }
    extra_sections = [
        s for s in sections
        if s["id"] not in standard_ids and s["id"] != "references"
    ]

    experience_roles: list[dict] = []
    for section in sections:
        if section["id"] == "experience":
            experience_roles = _extract_role_bullets(last_block)
            break

    avg_bullets = 0
    if experience_roles:
        avg_bullets = (
            sum(r["bullet_count"] for r in experience_roles)
            // len(experience_roles)
        )

    return {
        "sections": sections,
        "experience_roles": experience_roles,
        "total_sections": len(sections),
        "extra_sections": extra_sections,
        "avg_bullets_per_role": max(avg_bullets, 3),
        "section_ids": [s["id"] for s in sections],
    }
