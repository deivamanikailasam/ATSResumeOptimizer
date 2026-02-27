"""Coral Ribbon – Warm, approachable design with ribbon-style headers and rounded elements."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "coral_ribbon",
    "name": "Coral Ribbon",
    "description": "Warm ribbon-style section headers with rounded, approachable personality",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.20)
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
    line-height: 1.55;
    color: #3b3b3b;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    margin-bottom: 20px;
    padding-bottom: 12px;
    text-align: center;
}}

.resume-header h1 {{
    font-size: 30pt;
    font-weight: 300;
    color: {primary_color};
    margin-bottom: 4px;
}}

.contact-info {{
    display: block;
    margin-top: 6px;
    padding: 6px 0;
    border-top: 1px solid #e0e0e0;
    border-bottom: 1px solid #e0e0e0;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: #777;
    letter-spacing: 0.3px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: #ccc;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
}}

.resume-section h2 {{
    font-size: 9pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #fff;
    background: {primary_color};
    padding: 5px 14px;
    border-radius: 20px;
    margin-bottom: 10px;
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
    font-weight: 600;
    color: #2b2b2b;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: #999;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: {primary_color};
    font-weight: 500;
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 16px;
    margin-top: 3px;
}}

li {{
    font-size: 10pt;
    margin-bottom: 2.5px;
    color: #444;
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
    font-size: 9.5pt;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 3px 10px;
    border-radius: 14px;
    margin: 2px 3px 2px 0;
    font-size: 8.5pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 13px;
    padding-left: 12px;
    border-left: 3px solid {primary_light};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #555;
    padding: 10px 14px;
    background: {primary_light};
    border-radius: 8px;
    line-height: 1.6;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 0 4px 18px;
    font-size: 10pt;
    position: relative;
}}

.cert-list li::before {{
    content: "●";
    position: absolute;
    left: 2px;
    color: {primary_color};
    font-size: 7pt;
    top: 7px;
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
