"""PDF generation from fully-rendered HTML resumes using Playwright (Chromium).

Playwright uses a real browser engine so every CSS feature is supported:
pseudo-elements, :not(), flexbox, grid, @page, page-break-*, etc.

PDF generation runs in a subprocess to avoid event-loop conflicts with
Streamlit's asyncio loop.
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

_WORKER = Path(__file__).parent / "_pdf_worker.py"
_chromium_ready = False


def _ensure_chromium() -> None:
    """Install Playwright Chromium if the binary is not already present."""
    global _chromium_ready  # noqa: PLW0603
    if _chromium_ready:
        return

    # Allow TLS downloads behind corporate proxies that use self-signed certs
    env = {**os.environ, "NODE_TLS_REJECT_UNAUTHORIZED": "0"}

    subprocess.run(
        [sys.executable, "-m", "playwright", "install-deps", "chromium"],
        capture_output=True,
        text=True,
        env=env,
    )
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True,
        text=True,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Playwright browser install failed (exit {result.returncode}):\n"
            f"{result.stderr}"
        )
    _chromium_ready = True

# Print CSS injected into every resume for consistent PDF pagination.
_PAGE_BREAK_CSS = """\
<style>
/* ── Print optimizations (injected by pdf_export) ──────────────────────── */

.resume-section {
    margin-bottom: 10px !important;
    break-inside: auto !important;
    page-break-inside: auto !important;
}

.experience-item,
.education-item,
.project-item {
    margin-bottom: 8px !important;
    break-inside: auto !important;
    page-break-inside: auto !important;
}

h1, h2, h3 {
    break-after: avoid;
    page-break-after: avoid;
}

.item-header,
.company {
    break-after: avoid;
    page-break-after: avoid;
}

.experience-item ul,
.education-item ul,
.project-item p,
.project-item ul {
    break-before: avoid;
    page-break-before: avoid;
}

.resume-section:last-child,
.experience-item:last-child,
.education-item:last-child,
.project-item:last-child {
    margin-bottom: 0 !important;
}

.resume-header {
    page-break-after: avoid;
}

p, li {
    orphans: 2;
    widows: 2;
}

li {
    break-inside: avoid;
    page-break-inside: avoid;
}

.cert-list,
.skills-grid,
.summary {
    break-inside: auto !important;
    page-break-inside: auto !important;
}

.skill-category {
    break-inside: auto !important;
    page-break-inside: auto !important;
}

/* ── Generic fallback for extra/custom sections ────────────────────────── */
.resume-section:not(.summary):not(.skills):not(.experience):not(.education):not(.projects):not(.certifications) {
    margin-bottom: 10px !important;
    break-inside: auto !important;
    page-break-inside: auto !important;
}

.resume-section:not(.summary):not(.skills):not(.experience):not(.education):not(.projects):not(.certifications) h2 {
    font-size: 10pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding-bottom: 4px;
    margin-bottom: 8px;
    border-bottom: 1px solid #e0e0e0;
    break-after: avoid;
    page-break-after: avoid;
}

.resume-section:not(.summary):not(.skills):not(.experience):not(.education):not(.projects):not(.certifications) ul {
    padding-left: 16px;
    margin-top: 3px;
}

.resume-section:not(.summary):not(.skills):not(.experience):not(.education):not(.projects):not(.certifications) li {
    font-size: 10pt;
    margin-bottom: 2.5px;
}
</style>
"""


def _inject_page_break_css(html: str) -> str:
    """Inject page-break CSS into the HTML head to supplement template CSS."""
    if "</head>" in html:
        return html.replace("</head>", f"{_PAGE_BREAK_CSS}\n</head>", 1)
    return f"<html><head>{_PAGE_BREAK_CSS}</head><body>{html}</body></html>"


def html_to_pdf(html: str, output_path: Path) -> None:
    """Render HTML to PDF via headless Chromium in a subprocess.

    A subprocess is used so Playwright gets its own event loop, avoiding
    conflicts with Streamlit's asyncio loop on Windows.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _ensure_chromium()
    enhanced_html = _inject_page_break_css(html)

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    )
    try:
        tmp.write(enhanced_html)
        tmp.close()

        result = subprocess.run(
            [sys.executable, str(_WORKER), tmp.name, str(output_path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"PDF generation failed (exit {result.returncode}):\n{result.stderr}"
            )
    finally:
        Path(tmp.name).unlink(missing_ok=True)
