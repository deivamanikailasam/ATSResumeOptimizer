"""Ink Wash – East Asian sumi-e ink painting inspired, watercolor-style accents."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "ink_wash",
    "name": "Ink Wash",
    "description": "East Asian sumi-e ink painting inspired with watercolor-style accents",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.88)
    primary_dark = darken(primary_color, 0.25)
    sumi = "#1c1c1c"
    ink_gray = "#3d3d3d"
    diluted = "#8a8a8a"
    wash_light = "#f7f5f0"
    rice_paper = "#fdfcf8"
    stone = "#d6d0c4"
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
    font-family: 'Georgia', 'Palatino Linotype', 'Times New Roman', serif;
    font-size: 10pt;
    line-height: 1.6;
    color: {ink_gray};
    background: {rice_paper};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 18px 20px 14px;
    margin-bottom: 20px;
    border-bottom: 1px solid {stone};
    position: relative;
}}

.resume-header::after {{
    content: "〇";
    display: block;
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    background: {rice_paper};
    padding: 0 8px;
    color: {primary_color};
    font-size: 12pt;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 400;
    color: {sumi};
    letter-spacing: 6px;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {diluted};
    letter-spacing: 0.5px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ∣  ";
    color: {stone};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding-bottom: 4px;
}}

.resume-section h2 {{
    font-size: 11pt;
    font-weight: 400;
    color: {sumi};
    letter-spacing: 3px;
    margin-bottom: 10px;
    padding-bottom: 6px;
    text-align: center;
    position: relative;
}}

.resume-section h2::before,
.resume-section h2::after {{
    content: "───";
    color: {stone};
    font-size: 9pt;
    letter-spacing: -1px;
}}

.resume-section h2::before {{
    margin-right: 10px;
}}

.resume-section h2::after {{
    margin-left: 10px;
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
    color: {sumi};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {diluted};
    font-weight: 400;
    white-space: nowrap;
    font-style: italic;
}}

.company {{
    font-size: 9.5pt;
    color: {diluted};
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 16px;
    margin-top: 3px;
    list-style: none;
}}

ul li {{
    position: relative;
    padding-left: 4px;
}}

ul li::before {{
    content: "–";
    position: absolute;
    left: -14px;
    color: {primary_color};
    font-weight: 700;
}}

li {{
    font-size: 10pt;
    margin-bottom: 2px;
    color: {ink_gray};
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
    color: {sumi};
    display: block;
    margin-bottom: 3px;
    font-weight: 700;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_color};
    padding: 2px 10px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    border-bottom: 2px solid {primary_color};
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid {wash_light};
    page-break-inside: avoid;
}}

.experience-item:last-child,
.education-item:last-child,
.project-item:last-child {{
    border-bottom: none;
}}

.summary p {{
    font-size: 10pt;
    color: {ink_gray};
    text-align: center;
    font-style: italic;
    padding: 6px 16px;
    border-top: 1px solid {stone};
    border-bottom: 1px solid {stone};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    text-align: center;
}}

.cert-list li::before {{
    content: "⬥ ";
    color: {primary_color};
    font-size: 7pt;
    vertical-align: middle;
}}

.cert-list li:not(:last-child) {{
    border-bottom: 1px dotted {stone};
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
