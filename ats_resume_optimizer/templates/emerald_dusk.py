"""Garden Dusk – Rich colored header with light body, nature-inspired organic elegance."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "emerald_dusk",
    "name": "Garden Dusk",
    "description": "Rich colored header with light body, nature-inspired organic elegance",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_mid = lighten(primary_color, 0.75)
    primary_dark = darken(primary_color, 0.25)
    cream = "#fafdf8"
    bark = "#3d3229"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 10mm 14mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {bark};
    background: {cream};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    background: {primary_color};
    color: {cream};
    padding: 18px 22px 14px;
    margin-bottom: 18px;
    border-radius: 3px;
    position: relative;
}}

.resume-header::after {{
    content: "";
    display: block;
    width: 60px;
    height: 3px;
    background: {primary_mid};
    margin: 10px auto 0;
    border-radius: 2px;
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: {cream};
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
    text-align: center;
}}

.contact-info {{
    text-align: center;
}}

.contact-info span {{
    font-size: 9pt;
    color: {primary_light};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: {primary_mid};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
}}

.resume-section h2 {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    padding: 4px 10px;
    background: {primary_light};
    border-left: 4px solid {primary_color};
    border-radius: 0 3px 3px 0;
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
    color: {primary_dark};
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
    color: #6b7c65;
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
    color: {bark};
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
    color: {primary_dark};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_color};
    padding: 2px 9px;
    border-radius: 3px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
    border-bottom: 2px solid {primary_mid};
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-left: 12px;
    border-left: 2px solid {primary_mid};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #4a5545;
    padding: 8px 12px;
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
    border-bottom: 1px solid {primary_mid};
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
