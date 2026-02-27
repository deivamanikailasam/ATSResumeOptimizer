"""Arctic Frost – Crisp clean palette with gradient header, ultra-professional cold aesthetic."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "glacier_blue",
    "name": "Arctic Frost",
    "description": "Crisp clean palette with gradient header, ultra-professional cold aesthetic",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.25)
    frost_line = lighten(primary_color, 0.75)
    glacier_frost = lighten(primary_color, 0.95)
    deep_navy = "#152938"
    slate = "#4a5c6a"
    pure_white = "#ffffff"
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
    font-family: 'Calibri', 'Segoe UI', 'Helvetica Neue', sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {deep_navy};
    background: {pure_white};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 18px 20px 14px;
    margin-bottom: 16px;
    background: linear-gradient(135deg, {primary_color} 0%, {primary_dark} 100%);
    color: {pure_white};
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 300;
    color: {pure_white};
    letter-spacing: 2px;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {primary_light};
}}

.contact-info span:not(:last-child)::after {{
    content: "  │  ";
    color: rgba(255,255,255,0.4);
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding: 0 4px;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 600;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 2px solid {primary_color};
    position: relative;
}}

.resume-section h2::after {{
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 40px;
    height: 2px;
    background: {primary_dark};
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
    color: {deep_navy};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: {slate};
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
    color: #2d3e4e;
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
    color: {deep_navy};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 10px;
    border-radius: 3px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding: 8px 10px;
    background: {glacier_frost};
    border-radius: 3px;
    border-left: 3px solid {frost_line};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: {slate};
    padding: 6px 10px;
    background: {primary_light};
    border-radius: 3px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    border-bottom: 1px solid {frost_line};
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
