"""Midnight Luxe – Dark-header premium design with luxurious contrast and gold-style accents."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "midnight_luxe",
    "name": "Midnight Luxe",
    "description": "Dark header with luxurious contrast and premium accent tones",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.45)
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
    line-height: 1.5;
    color: #1a1a2e;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    background: {primary_dark};
    color: #fff;
    padding: 20px 24px 16px;
    margin-bottom: 20px;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 700;
    color: #fff;
    letter-spacing: 1px;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: {primary_light};
    letter-spacing: 0.4px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ▪  ";
    color: {primary_color};
    font-size: 6pt;
    vertical-align: middle;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
}}

.resume-section h2 {{
    font-size: 9pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: {primary_dark};
    padding-bottom: 5px;
    margin-bottom: 10px;
    border-bottom: 2px solid {primary_color};
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
    font-weight: 700;
    color: #1a1a2e;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {primary_color};
    font-weight: 600;
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
    margin-bottom: 2px;
    color: #2d2d44;
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 6px;
    font-size: 10pt;
}}

.skill-category strong {{
    color: {primary_dark};
    font-size: 9.5pt;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_dark};
    color: #fff;
    padding: 2px 9px;
    border-radius: 2px;
    margin: 1px 3px 1px 0;
    font-size: 8.5pt;
    font-weight: 500;
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
    color: #2d2d44;
    padding: 10px 14px;
    background: {primary_light};
    border-top: 2px solid {primary_color};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0 3px 18px;
    font-size: 10pt;
    position: relative;
}}

.cert-list li::before {{
    content: "✦";
    position: absolute;
    left: 0;
    color: {primary_color};
    font-size: 8pt;
    top: 5px;
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
