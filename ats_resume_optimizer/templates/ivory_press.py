"""Ivory Press – Editorial magazine-inspired layout with newspaper masthead header,
serif typography, thin horizontal rules, and refined typographic hierarchy."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "ivory_press",
    "name": "Ivory Press",
    "description": "Editorial magazine masthead with serif typography and typographic rules",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.93)
    primary_dark = darken(primary_color, 0.30)
    rule_color = lighten(primary_color, 0.55)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 14mm 18mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Georgia, 'Palatino Linotype', 'Book Antiqua', serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #222;
    background: #fff;
}}

/* ── Masthead header ───────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 18px 0 16px;
    border-top: 4px solid {primary_color};
    border-bottom: 1px solid {primary_color};
    margin-bottom: 8px;
    position: relative;
}}

.resume-header::after {{
    content: "";
    display: block;
    border-bottom: 4px solid {primary_color};
    margin-top: 3px;
}}

.resume-header h1 {{
    font-size: 30pt;
    font-weight: 400;
    color: #111;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-family: Georgia, 'Palatino Linotype', serif;
    margin-bottom: 8px;
    line-height: 1.1;
}}

.contact-info {{
    font-size: 8.5pt;
    color: #555;
    font-style: italic;
    letter-spacing: 0.5px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  |  ";
    color: {rule_color};
    font-style: normal;
}}

/* ── Sections ──────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding-top: 10px;
    border-top: 1px solid #ccc;
}}

.resume-section h2 {{
    font-size: 9pt;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: {primary_color};
    margin-bottom: 8px;
    text-align: center;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}}

/* ── Items ──────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 2px;
}}

.item-header h3 {{
    float: left;
    font-size: 10.5pt;
    font-weight: 700;
    color: #111;
    font-family: Georgia, serif;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: #666;
    font-style: italic;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: {primary_dark};
    margin-bottom: 3px;
    clear: both;
    font-variant: small-caps;
    letter-spacing: 0.5px;
}}

ul {{
    padding-left: 16px;
    margin-top: 4px;
}}

li {{
    font-size: 10pt;
    margin-bottom: 2px;
    color: #333;
    text-align: justify;
}}

li::marker {{
    color: {primary_color};
    font-size: 8pt;
}}

/* ── Skills ─────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
    column-count: 2;
    column-gap: 24px;
    column-rule: 1px solid #ddd;
}}

.skill-category {{
    margin-bottom: 6px;
    font-size: 10pt;
    break-inside: avoid;
}}

.skill-category strong {{
    color: {primary_dark};
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: block;
    margin-bottom: 2px;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}}

.skill-tag {{
    display: inline;
    font-size: 9.5pt;
    color: #333;
    font-family: Georgia, serif;
}}

.skill-tag:not(:last-child)::after {{
    content: ",  ";
}}

/* ── Experience / Education / Projects ──────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
    padding-bottom: 10px;
    border-bottom: 1px dotted #ddd;
}}

.experience-item:last-child,
.education-item:last-child,
.project-item:last-child {{
    border-bottom: none;
}}

.summary p {{
    font-size: 10pt;
    color: #333;
    text-align: justify;
    line-height: 1.65;
    font-style: italic;
    padding: 8px 16px;
    border-left: 2px solid {rule_color};
}}

/* ── Certifications ─────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
    column-count: 2;
    column-gap: 20px;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 9.5pt;
}}

.cert-list li::before {{
    content: "— ";
    color: {primary_color};
}}

/* ── Page-break safety ──────────────────────────────────────── */

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
