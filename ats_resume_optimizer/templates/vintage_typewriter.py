"""Vintage Typewriter – Retro monospace typewriter aesthetic with sepia tones."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "vintage_typewriter",
    "name": "Vintage Typewriter",
    "description": "Retro monospace typewriter aesthetic with sepia tones and inked borders",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_dark = darken(primary_color, 0.25)
    ink = "#2b2118"
    parchment = "#f5f0e8"
    aged_line = "#c4b49a"
    faded_ink = "#6e5c4e"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 14mm 16mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Courier New', 'Courier', 'Lucida Console', monospace;
    font-size: 10pt;
    line-height: 1.6;
    color: {ink};
    background: {parchment};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 3px double {aged_line};
    text-align: center;
}}

.resume-header h1 {{
    font-size: 22pt;
    font-weight: 700;
    color: {ink};
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: {faded_ink};
}}

.contact-info span:not(:last-child)::after {{
    content: "  //  ";
    color: {aged_line};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding-top: 2px;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 8px;
    padding-bottom: 3px;
    border-bottom: 1px dashed {aged_line};
}}

.resume-section h2::before {{
    content: ">> ";
    color: {aged_line};
}}

/* ── Items ───────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 1px;
}}

.item-header h3 {{
    float: left;
    font-size: 10pt;
    font-weight: 700;
    color: {ink};
    text-decoration: underline;
    text-underline-offset: 2px;
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_dark};
    font-weight: 400;
    white-space: nowrap;
}}

.company {{
    font-size: 9pt;
    color: {faded_ink};
    margin-bottom: 3px;
    clear: both;
    font-style: italic;
}}

ul {{
    padding-left: 20px;
    margin-top: 3px;
    list-style: none;
}}

ul li::before {{
    content: "- ";
    color: {primary_dark};
    font-weight: 700;
}}

li {{
    font-size: 9.5pt;
    margin-bottom: 2px;
    color: {ink};
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 6px;
    font-size: 9.5pt;
}}

.skill-category strong {{
    color: {ink};
    display: block;
    margin-bottom: 2px;
    text-decoration: underline;
    text-underline-offset: 2px;
}}

.skill-tag {{
    display: inline-block;
    background: transparent;
    color: {primary_dark};
    padding: 1px 6px;
    border: 1px solid {aged_line};
    margin: 1px 3px 1px 0;
    font-size: 8.5pt;
    font-family: 'Courier New', monospace;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 9.5pt;
    color: {primary_dark};
    border-left: 3px solid {aged_line};
    padding-left: 10px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 9.5pt;
    border-bottom: 1px dotted {aged_line};
}}

.cert-list li::before {{
    content: "* ";
    color: {primary_color};
    font-weight: 700;
}}

.cert-list li:last-child {{
    border-bottom: none;
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
