"""Anvil Forge – Industrial bold tones with strong geometric dividers."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "copper_forge",
    "name": "Anvil Forge",
    "description": "Industrial bold tones with strong geometric dividers and sturdy structure",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.88)
    primary_dark = darken(primary_color, 0.25)
    steel = "#3a3a3c"
    anvil = "#2c2c2e"
    iron_light = "#e8e4e0"
    warm_white = "#faf8f5"
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
    font-family: 'Trebuchet MS', 'Arial Narrow', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {steel};
    background: {warm_white};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 16px 18px;
    margin-bottom: 18px;
    background: {anvil};
    border-bottom: 4px solid {primary_color};
    position: relative;
}}

.resume-header::after {{
    content: "";
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 120px;
    height: 4px;
    background: {primary_color};
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 800;
    color: {primary_color};
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: #b0ada8;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ▪  ";
    color: {primary_color};
    font-size: 7pt;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 15px;
    padding-left: 14px;
    border-left: 4px solid {primary_color};
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 800;
    color: {anvil};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    background: linear-gradient(90deg, {iron_light} 0%, transparent 100%);
    padding: 4px 8px;
}}

.resume-section h2::before {{
    content: "■ ";
    color: {primary_color};
    font-size: 8pt;
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
    color: {anvil};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_color};
    font-weight: 700;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #706a62;
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
    color: {steel};
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
    color: {anvil};
    display: block;
    margin-bottom: 3px;
    font-weight: 800;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 9px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 700;
    border-left: 3px solid {primary_color};
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
    color: #504a42;
    padding-left: 8px;
    border-left: 3px solid {iron_light};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    border-bottom: 2px solid {iron_light};
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
