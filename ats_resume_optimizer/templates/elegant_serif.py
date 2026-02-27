"""Elegant Serif – Sophisticated serif typography inspired by editorial / luxury design."""

from ._colors import lighten

TEMPLATE = {
    "id": "elegant_serif",
    "name": "Elegant Serif",
    "description": "Refined serif typography with sophisticated spacing and accents",
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
    margin: 10mm 3mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: Georgia, 'Palatino Linotype', 'Book Antiqua', serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #2c2c2c;
}}

/* ── Top accent bar ─────────────────────────────────────────── */

.resume-container {{
    border-top: 4px solid {primary_color};
    padding-top: 20px;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    margin-bottom: 22px;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 400;
    color: {primary_color};
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-bottom: 10px;
}}

.contact-info {{
    text-align: center;
}}

.contact-info span {{
    font-size: 9pt;
    color: #777;
    font-style: italic;
}}

.contact-info span:not(:last-child)::after {{
    content: "   ◆   ";
    font-size: 5pt;
    vertical-align: middle;
    color: {primary_color};
    font-style: normal;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 17px;
}}

.resume-section h2 {{
    font-size: 11pt;
    font-style: italic;
    font-weight: 400;
    color: {primary_color};
    letter-spacing: 1.5px;
    padding-bottom: 4px;
    margin-bottom: 10px;
    border-bottom: 1px solid {primary_color};
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
    color: #1a1a1a;
}}

.item-header .date {{
    float: right;
    font-size: 9.5pt;
    color: #888;
    font-style: italic;
    white-space: nowrap;
}}

.company {{
    font-size: 10pt;
    color: #555;
    margin-bottom: 3px;
    clear: both;
    font-style: italic;
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
    margin-bottom: 5px;
    font-size: 10.5pt;
}}

.skill-category strong {{
    color: {primary_color};
    font-style: italic;
}}

.skill-tag {{
    color: #444;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item {{
    margin-bottom: 14px;
    page-break-inside: avoid;
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
    padding: 10px 14px;
    background: {primary_light};
    border-left: 3px solid {primary_color};
    font-style: italic;
    line-height: 1.6;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
    text-align: center;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10.5pt;
    font-style: italic;
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
