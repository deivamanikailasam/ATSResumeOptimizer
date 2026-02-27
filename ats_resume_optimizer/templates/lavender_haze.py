"""Dreamy Haze – Soft tinted palette with airy white floating card sections."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "lavender_haze",
    "name": "Dreamy Haze",
    "description": "Soft tinted palette with airy white floating card sections, dreamy elegance",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.25)
    primary_mist = lighten(primary_color, 0.97)
    deep_text = "#2d2640"
    muted_text = "#5e5478"
    cloud = "#ffffff"
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
    color: {deep_text};
    background: {primary_mist};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 20px 20px 16px;
    margin-bottom: 18px;
    background: {cloud};
    border-radius: 8px;
    border-top: 4px solid {primary_color};
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 300;
    color: {primary_dark};
    letter-spacing: 2px;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {muted_text};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: {primary_light};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding: 10px 14px;
    background: {cloud};
    border-radius: 6px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 600;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    padding-bottom: 5px;
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
    font-weight: 600;
    color: {deep_text};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_light};
    font-weight: 500;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: {muted_text};
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
    color: #3d3558;
}}

li::marker {{
    color: {primary_light};
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
    color: {deep_text};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 10px;
    border-radius: 14px;
    margin: 2px 3px 2px 0;
    font-size: 9pt;
    font-weight: 500;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid {primary_light};
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
    color: {muted_text};
    font-style: italic;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 0;
    font-size: 10pt;
    border-bottom: 1px solid {primary_light};
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
