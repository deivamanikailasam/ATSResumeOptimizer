"""Marble Hall – Elegant marble-inspired light textures with refined accents."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "marble_hall",
    "name": "Marble Hall",
    "description": "Elegant marble-inspired light palette with refined accents and sophistication",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.25)
    marble_white = "#faf9f7"
    marble_vein = "#e8e4df"
    warm_gray = "#6b6462"
    deep_text = "#2c2825"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 12mm 14mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Garamond', 'Georgia', 'Palatino Linotype', serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {deep_text};
    background: {marble_white};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 20px 24px 16px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, {marble_white} 0%, {marble_vein} 50%, {marble_white} 100%);
    border-bottom: 2px solid {primary_color};
    position: relative;
}}

.resume-header::before,
.resume-header::after {{
    content: "❖";
    position: absolute;
    bottom: -10px;
    color: {primary_color};
    font-size: 10pt;
    background: {marble_white};
    padding: 0 6px;
}}

.resume-header::before {{
    left: 45%;
}}

.resume-header::after {{
    display: none;
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 400;
    color: {primary_dark};
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 8px;
    font-style: italic;
}}

.contact-info span {{
    font-size: 9pt;
    color: {warm_gray};
    letter-spacing: 0.3px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  |  ";
    color: {primary_color};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding-bottom: 6px;
}}

.resume-section h2 {{
    font-size: 11pt;
    font-weight: 400;
    color: {primary_dark};
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 10px;
    padding-bottom: 5px;
    border-bottom: 1px solid {marble_vein};
    text-align: center;
    font-style: italic;
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
    color: {deep_text};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
    font-style: italic;
}}

.company {{
    font-size: 9.5pt;
    color: {warm_gray};
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
    color: #3d3835;
}}

li::marker {{
    color: {primary_color};
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
    color: {deep_text};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 10px;
    border-radius: 12px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
    border: 1px solid {lighten(primary_color, 0.6)};
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-left: 10px;
    border-left: 2px solid {marble_vein};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #3d3835;
    text-align: center;
    font-style: italic;
    padding: 0 20px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    border-bottom: 1px solid {marble_vein};
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
