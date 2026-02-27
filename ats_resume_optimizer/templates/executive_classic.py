"""Executive Classic – Traditional serif design inspired by Wall Street / consulting resumes."""

from ._colors import lighten

TEMPLATE = {
    "id": "executive_classic",
    "name": "Executive Classic",
    "description": "Traditional serif typography with formal, authoritative layout",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
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
    font-family: Georgia, 'Palatino Linotype', 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #222;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 3px double {primary_color};
}}

.resume-header h1 {{
    font-size: 24pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 4px;
    color: {primary_color};
    margin-bottom: 8px;
}}

.contact-info {{
    text-align: center;
}}

.contact-info span {{
    font-size: 9pt;
    color: #555;
}}

.contact-info span:not(:last-child)::after {{
    content: "  |  ";
    color: #aaa;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 15px;
}}

.resume-section h2 {{
    font-size: 11pt;
    font-variant: small-caps;
    letter-spacing: 2px;
    color: {primary_color};
    border-top: 1px solid {primary_color};
    border-bottom: 1px solid {primary_color};
    padding: 3px 0;
    margin-bottom: 10px;
    font-weight: 700;
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
    font-size: 10.5pt;
    font-weight: 700;
    color: #111;
    font-style: italic;
}}

.item-header .date {{
    float: right;
    font-size: 9.5pt;
    color: #666;
    font-style: italic;
    white-space: nowrap;
}}

.company {{
    font-size: 10pt;
    color: #333;
    font-weight: 600;
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 18px;
    margin-top: 3px;
}}

li {{
    font-size: 10.5pt;
    margin-bottom: 2.5px;
    color: #333;
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 4px;
    font-size: 10.5pt;
}}

.skill-category strong {{
    color: {primary_color};
}}

.skill-tag {{
    color: #333;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 13px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10.5pt;
    color: #333;
    text-align: justify;
    font-style: italic;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 2px 0;
    font-size: 10.5pt;
    text-align: center;
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
