"""Sahara Dune – Warm desert sand tones with bold accent highlights, sun-baked elegance."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "sahara_dune",
    "name": "Sahara Dune",
    "description": "Warm desert sand tones with bold accent highlights, sun-baked elegance",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.88)
    primary_dark = darken(primary_color, 0.2)
    sand = "#f5ede0"
    sand_deep = "#e6d8c3"
    dune_shadow = "#a89070"
    oasis = "#5c7a5e"
    clay = "#3d2e1e"
    warm_text = "#4a3828"
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
    font-family: 'Candara', 'Gill Sans', 'Segoe UI', sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {warm_text};
    background: {sand};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 16px 20px;
    margin-bottom: 18px;
    border-bottom: 3px solid {primary_color};
    background: linear-gradient(180deg, {sand} 0%, {sand_deep} 100%);
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: {clay};
    letter-spacing: 1px;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {dune_shadow};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ◦  ";
    color: {primary_color};
    font-size: 8pt;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 15px;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #fff;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    padding: 5px 12px;
    background: {primary_color};
    display: inline-block;
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
    color: {clay};
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
    color: {dune_shadow};
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
    color: {warm_text};
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
    color: {clay};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 9px;
    border-radius: 2px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-left: 12px;
    border-left: 3px solid {sand_deep};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: {dune_shadow};
    padding: 8px 14px;
    background: {sand_deep};
    border-radius: 3px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 0;
    font-size: 10pt;
    border-bottom: 1px solid {sand_deep};
}}

.cert-list li::before {{
    content: "✦ ";
    color: {primary_color};
    font-size: 7pt;
    vertical-align: middle;
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
