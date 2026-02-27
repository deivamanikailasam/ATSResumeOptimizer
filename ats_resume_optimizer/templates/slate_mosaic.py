"""Slate Mosaic – Cool gray with geometric mosaic-patterned dividers and ornaments."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "slate_mosaic",
    "name": "Slate Mosaic",
    "description": "Cool gray tones with geometric mosaic-patterned dividers and ornaments",
}


def _render(content_html: str, primary_color: str) -> str:
    slate = "#4a5568"
    slate_light = "#e2e6ec"
    slate_pale = "#f1f3f6"
    slate_dark = darken(slate, 0.25)
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.25)
    charcoal = "#1a202c"
    mid_gray = "#718096"
    white = "#ffffff"
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
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {charcoal};
    background: {white};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 16px 20px;
    margin-bottom: 6px;
    background: {slate};
    position: relative;
}}

.resume-header::after {{
    content: "◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇ ◆ ◇";
    display: block;
    text-align: center;
    font-size: 6pt;
    letter-spacing: 2px;
    color: {primary_color};
    background: {slate_pale};
    padding: 4px 0;
    overflow: hidden;
    white-space: nowrap;
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: {white};
    letter-spacing: 1px;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {slate_light};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ◆  ";
    color: {primary_color};
    font-size: 6pt;
    vertical-align: middle;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding: 0 4px;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: {slate};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    padding: 5px 10px;
    background: {slate_pale};
    border-left: 4px solid {primary_color};
    position: relative;
}}

.resume-section h2::after {{
    content: "◇◆◇";
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 6pt;
    color: {slate_light};
    letter-spacing: 2px;
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
    color: {charcoal};
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
    color: {mid_gray};
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
    color: #2d3748;
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
    color: {charcoal};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 9px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
    border-radius: 2px;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid {slate_light};
    page-break-inside: avoid;
}}

.experience-item:last-child,
.education-item:last-child,
.project-item:last-child {{
    border-bottom: none;
    padding-bottom: 0;
}}

.summary p {{
    font-size: 10pt;
    color: {mid_gray};
    padding-left: 12px;
    border-left: 3px solid {primary_color};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 8px;
    font-size: 10pt;
    margin-bottom: 3px;
    background: {slate_pale};
    border-left: 3px solid {slate_light};
}}

.cert-list li:last-child {{
    margin-bottom: 0;
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
