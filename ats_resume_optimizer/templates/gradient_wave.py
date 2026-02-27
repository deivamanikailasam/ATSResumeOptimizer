"""Gradient Wave – Modern gradient header with flowing SVG wave divider."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "gradient_wave",
    "name": "Gradient Wave",
    "description": "Bold gradient header with flowing wave divider, modern and vibrant",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.35)
    accent = darken(primary_color, 0.15)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 10mm 0;
}}
@page :first {{
    margin-top: 0;
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
    color: #1e1e2f;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    background: linear-gradient(135deg, {primary_color} 0%, {primary_dark} 100%);
    color: #fff;
    padding: 32px 32px 40px;
    position: relative;
}}

.resume-header::after {{
    content: "";
    display: block;
    position: absolute;
    bottom: -1px;
    left: 0;
    right: 0;
    height: 30px;
    background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 60'%3E%3Cpath d='M0 30 Q300 60 600 30 Q900 0 1200 30 L1200 60 L0 60Z' fill='%23ffffff'/%3E%3C/svg%3E") no-repeat bottom center;
    background-size: cover;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 800;
    color: #fff;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: rgba(255,255,255,0.85);
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: rgba(255,255,255,0.5);
}}

/* ── Body padding ───────────────────────────────────────────── */

.resume-section {{
    margin: 0 28px 14px;
}}

.resume-section:first-of-type {{
    margin-top: 18px;
}}

.resume-section h2 {{
    font-size: 10pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: {primary_dark};
    margin-bottom: 8px;
    padding-bottom: 4px;
    background: linear-gradient(90deg, {primary_color}, transparent);
    -webkit-background-clip: text;
    background-clip: text;
    border-bottom: 2px solid {primary_light};
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
    color: #1e1e2f;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {accent};
    font-weight: 600;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #666;
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
    color: #333;
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
    background: linear-gradient(135deg, {primary_light}, #fff);
    color: {primary_dark};
    padding: 2px 9px;
    border-radius: 12px;
    margin: 1px 3px 2px 0;
    font-size: 8.5pt;
    font-weight: 600;
    border: 1px solid {lighten(primary_color, 0.75)};
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
    color: #444;
    line-height: 1.6;
    padding: 10px 14px;
    background: {primary_light};
    border-radius: 6px;
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
    content: "◆";
    position: absolute;
    left: 0;
    color: {primary_color};
    font-size: 7pt;
    top: 6px;
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
