"""Swiss Grid – International Typographic Style with mathematical precision and strong grid."""

from ._colors import lighten

TEMPLATE = {
    "id": "swiss_grid",
    "name": "Swiss Grid",
    "description": "International Typographic Style with rigid grid and Helvetica precision",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.93)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 12mm 16mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.5;
    color: #111;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 4px solid #111;
}}

.resume-header h1 {{
    font-size: 36pt;
    font-weight: 900;
    color: #111;
    line-height: 1.05;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 8pt;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}}

.contact-info span:not(:last-child)::after {{
    content: "  /  ";
    color: #ccc;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding-top: 8px;
    border-top: 2px solid {primary_color};
}}

.resume-section h2 {{
    font-size: 7.5pt;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 4px;
    color: {primary_color};
    margin-bottom: 10px;
}}

/* ── Items ───────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 1px;
}}

.item-header h3 {{
    float: left;
    font-size: 10pt;
    font-weight: 700;
    color: #111;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}}

.item-header .date {{
    float: right;
    font-size: 8pt;
    color: #666;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    white-space: nowrap;
}}

.company {{
    font-size: 9pt;
    color: {primary_color};
    font-weight: 600;
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 14px;
    margin-top: 3px;
}}

li {{
    font-size: 9.5pt;
    margin-bottom: 2px;
    color: #222;
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 5px;
    font-size: 9.5pt;
}}

.skill-category strong {{
    color: #111;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: block;
    margin-bottom: 2px;
}}

.skill-tag {{
    display: inline-block;
    color: #111;
    border-bottom: 1px solid {primary_color};
    padding: 0 1px 1px;
    margin: 1px 8px 1px 0;
    font-size: 9pt;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 9.5pt;
    color: #222;
    padding: 8px 0;
    border-left: 4px solid {primary_color};
    padding-left: 12px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 9.5pt;
    border-bottom: 1px solid #eee;
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
