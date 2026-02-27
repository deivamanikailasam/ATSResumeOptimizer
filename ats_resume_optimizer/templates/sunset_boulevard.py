"""Sunset Boulevard – Warm gradient tones with smooth color transitions and horizon backdrop."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "sunset_boulevard",
    "name": "Sunset Boulevard",
    "description": "Warm gradient tones with smooth color transitions and horizon backdrop",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.15)
    dusk = "#2d1b3d"
    twilight = "#3d2848"
    horizon = "#f9f5f0"
    warm_text = "#3a2520"
    muted = "#7a6055"
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
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {warm_text};
    background: {horizon};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 20px 22px 16px;
    margin-bottom: 18px;
    background: linear-gradient(135deg, {primary_color} 0%, {primary_dark} 60%, {twilight} 100%);
    border-radius: 4px;
    position: relative;
}}

.resume-header::after {{
    content: "";
    display: block;
    height: 3px;
    background: linear-gradient(90deg, {primary_color}, {primary_dark}, {primary_color});
    margin-top: 10px;
    border-radius: 2px;
    opacity: 0.5;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 300;
    color: #ffffff;
    letter-spacing: 2px;
    margin-bottom: 5px;
    text-shadow: 0 1px 4px rgba(0,0,0,0.15);
}}

.contact-info span {{
    font-size: 9pt;
    color: rgba(255,255,255,0.85);
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: rgba(255,255,255,0.4);
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 15px;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: {primary_dark};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 2px solid transparent;
    border-image: linear-gradient(90deg, {primary_color}, {primary_dark}) 1;
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
    color: {warm_text};
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
    color: {muted};
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
    color: #4a3530;
}}

li::marker {{
    color: {primary_dark};
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
    color: {warm_text};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: linear-gradient(135deg, {primary_light}, {primary_light});
    color: {primary_dark};
    padding: 2px 10px;
    border-radius: 14px;
    margin: 2px 3px 2px 0;
    font-size: 9pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-left: 12px;
    border-left: 3px solid {primary_light};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: {muted};
    padding: 8px 14px;
    background: linear-gradient(135deg, {primary_light}, {primary_light});
    border-radius: 4px;
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

.cert-list li::before {{
    content: "☀ ";
    color: {primary_color};
    font-size: 8pt;
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
