"""Bamboo Zen – Natural earth tones, minimalist zen garden peacefulness."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "bamboo_zen",
    "name": "Bamboo Zen",
    "description": "Natural earth tones with minimalist zen garden peacefulness and calm flow",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.88)
    primary_dark = darken(primary_color, 0.3)
    tatami = "#f6f2ea"
    shoji = "#ffffff"
    pebble = "#8c8478"
    earth = "#3c3529"
    wood = "#6b5d4f"
    sand_garden = "#e8e2d6"
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
    font-family: 'Optima', 'Segoe UI', 'Helvetica Neue', sans-serif;
    font-size: 10pt;
    line-height: 1.65;
    color: {earth};
    background: {tatami};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 20px 20px 18px;
    margin-bottom: 20px;
}}

.resume-header h1 {{
    font-size: 24pt;
    font-weight: 400;
    color: {primary_dark};
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.resume-header::after {{
    content: "";
    display: block;
    width: 80px;
    height: 1px;
    background: {primary_color};
    margin: 6px auto 0;
}}

.contact-info span {{
    font-size: 9pt;
    color: {pebble};
    letter-spacing: 0.5px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: {sand_garden};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 18px;
}}

.resume-section h2 {{
    font-size: 10pt;
    font-weight: 400;
    color: {primary_color};
    text-transform: lowercase;
    letter-spacing: 4px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid {sand_garden};
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
    color: {earth};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {pebble};
    font-weight: 400;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: {wood};
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 14px;
    margin-top: 3px;
    list-style: none;
}}

ul li {{
    position: relative;
    padding-left: 6px;
}}

ul li::before {{
    content: "○";
    position: absolute;
    left: -12px;
    color: {primary_color};
    font-size: 7pt;
    top: 3px;
}}

li {{
    font-size: 10pt;
    margin-bottom: 3px;
    color: {earth};
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 8px;
    font-size: 10pt;
}}

.skill-category strong {{
    color: {primary_dark};
    display: block;
    margin-bottom: 3px;
    font-weight: 600;
    letter-spacing: 1px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 3px 12px;
    border-radius: 20px;
    margin: 2px 4px 2px 0;
    font-size: 9pt;
    font-weight: 500;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid {sand_garden};
    page-break-inside: avoid;
}}

.experience-item:last-child,
.education-item:last-child,
.project-item:last-child {{
    border-bottom: none;
    padding-bottom: 0;
}}

.summary p {{
    font-size: 10pt;
    color: {wood};
    text-align: center;
    letter-spacing: 0.3px;
    padding: 0 30px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 0;
    font-size: 10pt;
    text-align: center;
    color: {earth};
}}

.cert-list li::before {{
    content: "· ";
    color: {primary_color};
}}

.cert-list li:not(:last-child) {{
    border-bottom: 1px solid {sand_garden};
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
