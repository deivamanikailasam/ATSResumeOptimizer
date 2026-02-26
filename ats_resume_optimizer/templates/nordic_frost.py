"""Nordic Frost – Scandinavian-inspired minimalism with cool geometry and airy spacing."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "nordic_frost",
    "name": "Nordic Frost",
    "description": "Scandinavian minimalism with geometric accents and airy spacing",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.94)
    primary_muted = lighten(primary_color, 0.75)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 15mm 18mm;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #2e3440;
    background: #fff;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    margin-bottom: 24px;
    padding: 18px 20px 14px;
    background: {primary_light};
    border-top: 3px solid {primary_color};
    border-bottom: 1px solid {primary_muted};
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 200;
    color: {primary_color};
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: #6b7280;
    letter-spacing: 0.8px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ——  ";
    color: {primary_muted};
    font-size: 7pt;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 18px;
}}

.resume-section h2 {{
    font-size: 8pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 3.5px;
    color: {primary_color};
    margin-bottom: 10px;
    padding-bottom: 6px;
    position: relative;
}}

.resume-section h2::after {{
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 40px;
    height: 2px;
    background: {primary_color};
}}

/* ── Items ───────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 2px;
}}

.item-header h3 {{
    float: left;
    font-size: 10.5pt;
    font-weight: 600;
    color: #1f2937;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: #9ca3af;
    letter-spacing: 0.5px;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #6b7280;
    margin-bottom: 4px;
    clear: both;
}}

ul {{
    padding-left: 15px;
    margin-top: 4px;
}}

li {{
    font-size: 10pt;
    margin-bottom: 3px;
    color: #374151;
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
    color: #1f2937;
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: #374151;
    padding: 2px 10px;
    margin: 2px 4px 2px 0;
    font-size: 9pt;
    border-left: 2px solid {primary_color};
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 14px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #4b5563;
    padding: 10px 16px;
    background: {primary_light};
    border-left: 3px solid {primary_color};
    line-height: 1.65;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 0 4px 16px;
    font-size: 10pt;
    position: relative;
}}

.cert-list li::before {{
    content: "◇";
    position: absolute;
    left: 0;
    color: {primary_color};
    font-size: 9pt;
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
