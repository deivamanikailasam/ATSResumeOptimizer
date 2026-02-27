"""Bold Tide – Bold dark header with charcoal, commanding authority feel."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "crimson_tide",
    "name": "Bold Tide",
    "description": "Bold dark header with charcoal tones, commanding authority and power",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.2)
    charcoal = "#2b2b2b"
    charcoal_soft = "#3e3e3e"
    smoke = "#f4f3f2"
    ash = "#717171"
    pure_white = "#ffffff"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 12mm 14mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {charcoal};
    background: {pure_white};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 16px 20px;
    margin-bottom: 16px;
    background: {charcoal};
    border-top: 5px solid {primary_color};
    position: relative;
}}

.resume-header::after {{
    content: "";
    position: absolute;
    bottom: 0;
    right: 0;
    width: 80px;
    height: 5px;
    background: {primary_color};
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 800;
    color: {pure_white};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: #b0b0b0;
}}

.contact-info span:not(:last-child)::after {{
    content: "  //  ";
    color: {primary_color};
    font-weight: 700;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 15px;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 800;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 3px solid {charcoal};
    position: relative;
}}

.resume-section h2::after {{
    content: "";
    position: absolute;
    bottom: -3px;
    left: 0;
    width: 50px;
    height: 3px;
    background: {primary_color};
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
    color: {charcoal};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_color};
    font-weight: 700;
    white-space: nowrap;
    text-transform: uppercase;
}}

.company {{
    font-size: 9.5pt;
    color: {ash};
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
    color: #3a3a3a;
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
    font-weight: 800;
}}

.skill-tag {{
    display: inline-block;
    background: {charcoal};
    color: {pure_white};
    padding: 2px 9px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
    border-left: 3px solid {primary_color};
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-left: 12px;
    border-left: 2px solid {smoke};
    page-break-inside: avoid;
}}

.experience-item:hover,
.education-item:hover,
.project-item:hover {{
    border-left-color: {primary_color};
}}

.summary p {{
    font-size: 10pt;
    color: {charcoal_soft};
    padding: 8px 14px;
    border-left: 4px solid {primary_color};
    background: {primary_light};
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
    background: {smoke};
    border-left: 3px solid {primary_color};
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
