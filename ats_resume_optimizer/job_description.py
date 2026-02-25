"""Job description fetching from text or URL."""

import requests
from bs4 import BeautifulSoup


def fetch_jd_from_url(url: str) -> str:
    """Fetch and extract job description text from a URL."""
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    candidates = [
        soup.find("article"),
        soup.find("section", {"class": "job-description"}),
        soup.find("div", {"class": "description"}),
        soup.body,
    ]
    for c in candidates:
        if c:
            text = " ".join(c.get_text(separator="\n").split())
            if len(text) > 500:
                return text

    return " ".join(soup.get_text(separator="\n").split())


def get_job_description(
    jd_text: str | None = None, jd_url: str | None = None
) -> str:
    """Return job description from provided text or by fetching from URL."""
    if jd_text:
        return jd_text.strip()
    if jd_url:
        return fetch_jd_from_url(jd_url)
    raise ValueError("Provide either job description text or a job URL.")
