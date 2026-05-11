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


def _is_letter_spaced_token(tok: str) -> bool:
    """Return True if token looks like part of a letter-spaced word.

    Tokens are 1–3 uppercase alpha characters:
    - 1-char  → the common case ("E", "D", "U", "C", …)
    - 2-char  → ligature pairs some PDF fonts keep as a single glyph
                (e.g. "TA", "AT", "RY", "TI")
    - 3-char  → larger kerning groups some fonts emit as one unit
                (e.g. "AWA" from "AWARDS", "CER" from "CERTIFICATIONS",
                 "PRO" from "PROFESSIONAL")
    All must be strictly uppercase so common lowercase words ("the", "a")
    never trigger detection.
    """
    return 1 <= len(tok) <= 3 and tok.isalpha() and tok == tok.upper()


def _collapse_letter_spaced_line(line: str) -> str:
    """Collapse letter-spaced section-header text back into normal words.

    Many PDFs apply decorative character spacing to section headers.
    pypdf layout mode extracts these as space-separated tokens where each
    token is 1–2 uppercase chars (ligature pairs stay together):

        "PROFESSIONAL S U M M A RY"   → "PROFESSIONAL SUMMARY"
        "N O TA B L E PROJECTS"       → "NOTABLE PROJECTS"
        "E D U C AT I O N"            → "EDUCATION"

    Algorithm:
    - Scan tokens left-to-right (splitting on every single space, so
      double-space gaps produce an empty-string token that acts as a
      natural sequence breaker).
    - Accumulate consecutive 1–2 uppercase-alpha tokens into a run.
    - When the run ends, collapse it into one word if it is ≥ 3 tokens
      long AND produces a result of ≥ 4 characters.  The dual threshold
      avoids merging legitimate short runs like "I", "A", "UK US".
    - Non-letter-spaced tokens (normal words, punctuation, numbers) are
      passed through unchanged.
    """
    stripped = line.strip()
    if not stripped:
        return line

    tokens = stripped.split(" ")          # NB: double-space → empty string token
    result: list[str] = []
    run: list[str] = []

    def _flush_run() -> None:
        collapsed = "".join(run)
        # Collapse only when: ≥4 tokens AND result is ≥4 chars.
        # The 4-token floor stops 3-letter abbreviation triplets
        # (e.g. "API REST SQL") from merging into one mangled word.
        if len(run) >= 4 and len(collapsed) >= 4:
            result.append(collapsed)
        else:
            result.extend(run)
        run.clear()

    for tok in tokens:
        if _is_letter_spaced_token(tok):
            run.append(tok)
        else:
            if run:
                _flush_run()
            result.append(tok)

    if run:
        _flush_run()

    leading = len(line) - len(line.lstrip())
    # Filter out empty-string artefacts from double-space splits before joining.
    words = [t for t in result if t != ""]
    return " " * leading + " ".join(words)


def _normalize_layout_text(text: str) -> str:
    """Remove visual-positioning artifacts left by pypdf's layout extraction.

    Layout mode inserts spaces between characters and words to approximate
    their horizontal positions on the page.  Those extra spaces pass through
    verbatim into LLM prompts and produce broken spacing in the generated HTML.

    Normalisation pipeline (order matters):
    1. Collapse letter-spaced words FIRST, while 2-space word boundaries are
       still intact (e.g. "E X P E R I E N C E" → "EXPERIENCE").
    2. Collapse any remaining run of 2+ spaces on a line to one space.
    3. Strip trailing whitespace.
    4. Strip leading bullet/list characters from each line — these are PDF
       rendering artefacts that become double-bullets when the LLM wraps
       the same text inside <li> tags.
    5. Collapse runs of 3+ consecutive blank lines to one blank line
       (keeps meaningful section breaks without visual padding noise).
    """
    lines = text.split("\n")

    # Step 1 — fix letter-spaced section headers before multi-space collapse.
    lines = [_collapse_letter_spaced_line(line) for line in lines]

    # Step 2 & 3 — collapse remaining multi-spaces and strip trailing space.
    cleaned: list[str] = [re.sub(r" {2,}", " ", ln).rstrip() for ln in lines]

    # Step 4 — strip leading bullet/list characters.
    # These are visual markers in the PDF that HTML <li> already provides.
    # We deliberately exclude "-" and "*" because they appear legitimately
    # inside dates ("Jan 2020 - Mar 2022") and emphasis text.
    _BULLET_CHARS = re.compile(r"^[\s]*[•·◦▪▸▹►▶●○◉‣⁃–—]\s*")
    cleaned = [_BULLET_CHARS.sub("", ln) for ln in cleaned]

    # Step 5 — deduplicate consecutive blank lines.
    result: list[str] = []
    blank_run = 0
    for line in cleaned:
        if not line.strip():
            blank_run += 1
            if blank_run <= 1:
                result.append("")
        else:
            blank_run = 0
            result.append(line)

    return "\n".join(result)


def _extract_page_text(page) -> str:
    """Extract text from a single PDF page, preserving visual reading order.

    Strategy:
    1. Use layout mode — sorts characters by Y/X visual position so sections
       appear top-to-bottom as seen on screen (fixes mis-ordered sections).
    2. Normalize the layout-mode output to remove extra spaces that the mode
       inserts for visual character alignment (fixes word/sentence spacing).
    3. Fall back to plain extraction if layout mode returns nothing.
    """
    try:
        text = page.extract_text(extraction_mode="layout") or ""
        if text.strip():
            return _normalize_layout_text(text)
    except Exception:
        pass
    return page.extract_text() or ""


def extract_resume_text(pdf_path: Path) -> str:
    """Extract text from a resume PDF in visual reading order.

    Raises ValueError if no text is found (e.g. scanned/image-only PDF).
    """
    reader = PdfReader(str(pdf_path))
    pages_text = [_extract_page_text(page) for page in reader.pages]
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
