"""Creative Bold – Striking left-accent design inspired by modern design portfolios."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "creative_bold",
    "name": "Creative Bold",
    "description": "Bold accents, colored left borders, skill tags with modern flair",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.25)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 16mm 18mm;
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
    color: #1a1a1a;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    margin-bottom: 20px;
    padding: 14px 16px;
    border-left: 5px solid {primary_color};
    background-color: {primary_light};
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 800;
    color: #1a1a1a;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: #555;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: #999;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding-left: 14px;
    border-left: 3px solid {primary_color};
}}

.resume-section h2 {{
    font-size: 11pt;
    font-weight: 800;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
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
    color: #111;
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
    color: #555;
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
    color: #1a1a1a;
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 8px;
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
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #333;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    border-bottom: 1px dashed #ddd;
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
