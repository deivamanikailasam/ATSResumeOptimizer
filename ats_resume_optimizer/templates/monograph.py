"""Monograph – Editorial publication-inspired layout with typographic sophistication."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "monograph",
    "name": "Monograph",
    "description": "Editorial magazine-inspired layout with refined typographic hierarchy",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.93)
    primary_dark = darken(primary_color, 0.30)
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
    font-family: Georgia, 'Palatino Linotype', 'Book Antiqua', serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #222;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    margin-bottom: 22px;
    text-align: center;
    padding-bottom: 16px;
}}

.resume-header h1 {{
    font-size: 32pt;
    font-weight: 400;
    color: #111;
    letter-spacing: 2px;
    margin-bottom: 2px;
    border-bottom: 1px solid #111;
    display: inline-block;
    padding-bottom: 4px;
}}

.contact-info {{
    margin-top: 10px;
}}

.contact-info span {{
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 8pt;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 1.5px;
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
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 8pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #fff;
    background: {primary_color};
    padding: 4px 0;
    margin-bottom: 11px;
    text-align: center;
}}

/* ── Items ───────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 1px;
}}

.item-header h3 {{
    float: left;
    font-size: 11pt;
    font-weight: 700;
    color: #111;
}}

.item-header .date {{
    float: right;
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 8pt;
    color: {primary_color};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #666;
    font-style: italic;
    margin-bottom: 4px;
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
    margin-bottom: 5px;
    font-size: 10pt;
}}

.skill-category strong {{
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: {primary_dark};
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.skill-tag {{
    color: #333;
    font-size: 10pt;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item {{
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    page-break-inside: avoid;
}}

.experience-item:last-child {{
    border-bottom: none;
}}

.education-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10.5pt;
    color: #444;
    text-align: justify;
    line-height: 1.7;
    font-style: italic;
    padding: 8px 0;
    border-top: 1px solid {primary_color};
    border-bottom: 1px solid {primary_color};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
    text-align: center;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
}}

.cert-list li:not(:last-child)::after {{
    content: "";
    display: block;
    width: 30px;
    height: 1px;
    background: {primary_color};
    margin: 4px auto 0;
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
