"""PDF generation from fully-rendered HTML resumes using Playwright (Chromium).

Playwright uses a real browser engine so every CSS feature is supported:
pseudo-elements, :not(), flexbox, grid, @page, page-break-*, etc.

PDF generation runs in a subprocess to avoid event-loop conflicts with
Streamlit's asyncio loop.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

_WORKER = Path(__file__).parent / "_pdf_worker.py"

# Page-break CSS injected into every resume for print safety
_PAGE_BREAK_CSS = """\
<style>
/* ── Print optimizations (injected by pdf_export) ──────────────────────── */

.experience-item,
.education-item,
.project-item {
    page-break-inside: avoid;
}

h1, h2, h3 {
    page-break-after: avoid;
}

.resume-header {
    page-break-after: avoid;
}

p, li {
    orphans: 3;
    widows: 3;
}

.cert-list,
.skills-grid,
.summary {
    page-break-inside: avoid;
}

.skill-category {
    page-break-inside: avoid;
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
