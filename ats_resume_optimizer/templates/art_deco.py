"""Art Deco – 1920s-inspired geometric borders with elegant luxury accents."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "art_deco",
    "name": "Art Deco",
    "description": "1920s-inspired geometric borders with elegant luxury styling",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.35)
    gold_tint = lighten(primary_color, 0.70)
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
    font-family: Georgia, 'Times New Roman', 'Palatino Linotype', serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1a1a1a;
}}

.resume-container {{
    border: 3px double {primary_color};
    padding: 6px;
}}

.resume-container > * {{
    border: 1px solid {gold_tint};
    padding: 0;
}}

.resume-container > *:not(:last-child) {{
    border-bottom: none;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 22px 20px 16px;
    background: {primary_light};
    position: relative;
}}

.resume-header::before,
.resume-header::after {{
    content: "◆◆◆";
    display: block;
    letter-spacing: 12px;
    color: {primary_color};
    font-size: 8pt;
}}

.resume-header::before {{
    margin-bottom: 10px;
}}

.resume-header::after {{
    margin-top: 10px;
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 400;
    color: {primary_dark};
    text-transform: uppercase;
    letter-spacing: 5px;
    margin-bottom: 6px;
    font-family: Georgia, 'Palatino Linotype', serif;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: #555;
    font-style: italic;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ◇  ";
    color: {primary_color};
    font-style: normal;
    font-size: 7pt;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    padding: 14px 20px;
}}

.resume-section h2 {{
    font-size: 10pt;
    font-weight: 400;
    text-transform: uppercase;
    letter-spacing: 4px;
    color: {primary_dark};
    text-align: center;
    margin-bottom: 10px;
    position: relative;
    padding-bottom: 8px;
}}

.resume-section h2::after {{
    content: "";
    position: absolute;
    bottom: 0;
    left: 30%;
    right: 30%;
    height: 1px;
    background: linear-gradient(90deg, transparent, {primary_color}, transparent);
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
    font-family: Georgia, serif;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {primary_color};
    font-weight: 400;
    font-style: italic;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #666;
    margin-bottom: 3px;
    clear: both;
    font-style: italic;
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

li::marker {{
    color: {primary_color};
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
    text-align: center;
}}

.skill-category {{
    margin-bottom: 6px;
    font-size: 10pt;
}}

.skill-category strong {{
    color: {primary_dark};
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 10px;
    margin: 1px 2px;
    font-size: 8.5pt;
    font-weight: 400;
    border: 1px solid {gold_tint};
    letter-spacing: 0.5px;
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
    text-align: center;
    font-style: italic;
    line-height: 1.65;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
    text-align: center;
}}

.cert-list li {{
    padding: 4px 0;
    font-size: 10pt;
}}

.cert-list li::before {{
    content: "◈ ";
    color: {primary_color};
    font-size: 8pt;
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
