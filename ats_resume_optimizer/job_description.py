"""Job description fetching from text or URL."""

import re

import requests
from bs4 import BeautifulSoup

_BOILERPLATE_RE = [
    re.compile(r"equal\s+opportunity\s+employer", re.IGNORECASE),
    re.compile(
        r"we\s+(?:are|is)\s+(?:an?\s+)?(?:EOE|EEO|equal\s+opportunity)",
        re.IGNORECASE,
    ),
    re.compile(
        r"regardless\s+of\s+race,?\s+color,?\s+religion,?\s+sex",
        re.IGNORECASE,
    ),
    re.compile(
        r"applicants?\s+(?:are|will\s+be)\s+considered\s+"
        r"(?:for\s+employment\s+)?without\s+regard",
        re.IGNORECASE,
    ),
]


def _clean_jd_text(text: str) -> str:
    """Remove obvious EEO / legal boilerplate paragraphs from JD text."""
    paragraphs = re.split(r"\n{2,}", text)
    cleaned = [p for p in paragraphs if not any(r.search(p) for r in _BOILERPLATE_RE)]
    return "\n\n".join(cleaned).strip()


def fetch_jd_from_url(url: str) -> str:
    """Fetch and extract job description text from a URL."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, timeout=15, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    candidates = [
        soup.find("article"),
        soup.find("section", {"class": re.compile(r"job[-_]?desc", re.I)}),
        soup.find("div", {"class": re.compile(r"job[-_]?desc", re.I)}),
        soup.find("div", {"class": re.compile(r"description", re.I)}),
        soup.find("div", {"id": re.compile(r"job[-_]?desc", re.I)}),
        soup.find("div", {"id": re.compile(r"description", re.I)}),
        # Greenhouse
        soup.find("div", {"id": "content"}),
        # Lever
        soup.find("div", {"class": "posting-page"}),
        soup.find("div", {"class": re.compile(r"posting", re.I)}),
        # Workday
        soup.find("div", attrs={"data-automation-id": "jobPostingDescription"}),
        # LinkedIn
        soup.find("div", {"class": re.compile(r"show-more-less", re.I)}),
        soup.find("div", {"class": re.compile(r"jobs-description", re.I)}),
        # Indeed
        soup.find("div", {"id": "jobDescriptionText"}),
        # Generic fallback
        soup.find("main"),
        soup.body,
    ]

    for c in candidates:
        if c:
            text = " ".join(c.get_text(separator="\n").split())
            if len(text) > 500:
                return _clean_jd_text(text)

    return _clean_jd_text(" ".join(soup.get_text(separator="\n").split()))


def get_job_description(
    jd_text: str | None = None, jd_url: str | None = None
) -> str:
    """Return job description from provided text or by fetching from URL."""
    if jd_text:
        return jd_text.strip()
    if jd_url:
        return fetch_jd_from_url(jd_url)
    raise ValueError("Provide either job description text or a job URL.")
