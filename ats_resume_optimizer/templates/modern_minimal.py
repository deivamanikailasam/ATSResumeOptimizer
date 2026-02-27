"""Modern Minimal – Clean, whitespace-rich design inspired by Apple/Airbnb aesthetics."""

from ._colors import lighten

TEMPLATE = {
    "id": "modern_minimal",
    "name": "Modern Minimal",
    "description": "Clean lines, generous whitespace, subtle color accents",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 10mm 3mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #2d2d2d;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    margin-bottom: 22px;
    padding-bottom: 14px;
    border-bottom: 2px solid {primary_color};
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 300;
    color: {primary_color};
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: #ccc;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 17px;
}}

.resume-section h2 {{
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: {primary_color};
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 4px;
    margin-bottom: 10px;
    font-weight: 600;
}}

/* ── Items ───────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 1px;
}}

.item-header h3 {{
    float: left;
    font-size: 10.5pt;
    font-weight: 600;
    color: #1a1a1a;
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: #888;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #555;
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 16px;
    margin-top: 3px;
}}

li {{
    font-size: 10pt;
    margin-bottom: 2.5px;
    color: #333;
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 4px;
    font-size: 10pt;
}}

.skill-category strong {{
    color: #1a1a1a;
}}

.skill-tag {{
    color: #444;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #444;
    background: {primary_light};
    padding: 8px 12px;
    border-radius: 4px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 2px 0;
    font-size: 10pt;
}}

/* ── Page-break safety ───────────────────────────────────────── */

h2, h3 {{
    page-break-after: avoid;
}}
</style>
</head>
<body>
<div class="resume-container">
{content_html}
</div>
</body>
</html>"""


TEMPLATE["render"] = _render
