"""Brushstroke – Watercolour / painterly design with artistic brush-stroke accents,
soft washed backgrounds, and a creative atelier aesthetic."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "brushstroke",
    "name": "Brushstroke",
    "description": "Watercolour-inspired artistic accents with painterly wash backgrounds",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_wash = lighten(primary_color, 0.85)
    primary_faint = lighten(primary_color, 0.95)
    primary_dark = darken(primary_color, 0.30)
    stroke_mid = lighten(primary_color, 0.50)
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
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #222;
    background: #fff;
}}

/* ── Header (watercolour wash) ─────────────────────────────── */

.resume-header {{
    padding: 28px 26px 22px;
    position: relative;
    background:
        radial-gradient(ellipse at 15% 50%, {primary_wash}cc 0%, transparent 55%),
        radial-gradient(ellipse at 85% 30%, {primary_light}aa 0%, transparent 50%),
        radial-gradient(ellipse at 50% 90%, {primary_faint} 0%, transparent 60%);
    border-bottom: none;
}}

.resume-header::after {{
    content: "";
    position: absolute;
    bottom: 0;
    left: 5%;
    right: 5%;
    height: 3px;
    background: linear-gradient(
        90deg,
        transparent,
        {primary_color}88,
        {stroke_mid},
        {primary_color}88,
        transparent
    );
    border-radius: 2px;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 300;
    color: {primary_dark};
    letter-spacing: 1px;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: #555;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ~  ";
    color: {stroke_mid};
}}

/* ── Sections ──────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding: 0 8px;
}}

.resume-section h2 {{
    font-size: 10pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: {primary_dark};
    margin-bottom: 10px;
    padding: 4px 14px;
    position: relative;
    display: inline-block;
}}

.resume-section h2::before {{
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 8px;
    background: {primary_wash};
    border-radius: 3px;
    z-index: -1;
    transform: skewX(-6deg);
}}

/* ── Items ──────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 2px;
}}

.item-header h3 {{
    float: left;
    font-size: 10.5pt;
    font-weight: 700;
    color: #1a1a1a;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {stroke_mid};
    font-weight: 600;
    white-space: nowrap;
    font-style: italic;
}}

.company {{
    font-size: 9.5pt;
    color: #666;
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
    color: #333;
}}

li::marker {{
    color: {stroke_mid};
}}

/* ── Skills ─────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 7px;
    font-size: 10pt;
}}

.skill-category strong {{
    color: {primary_dark};
    font-size: 9pt;
    display: block;
    margin-bottom: 3px;
    font-style: italic;
}}

.skill-tag {{
    display: inline-block;
    background: linear-gradient(135deg, {primary_faint}, {primary_light});
    color: {primary_dark};
    padding: 2px 10px;
    border-radius: 3px;
    margin: 2px 4px 2px 0;
    font-size: 8.5pt;
    font-weight: 600;
    border-bottom: 2px solid {primary_wash};
}}

/* ── Experience / Education / Projects ──────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 14px;
    page-break-inside: avoid;
    padding: 8px 14px;
    position: relative;
    border-left: 3px solid transparent;
    border-image: linear-gradient(
        to bottom,
        {primary_color},
        {stroke_mid},
        transparent
    ) 1;
}}

.summary p {{
    font-size: 10pt;
    color: #444;
    line-height: 1.65;
    padding: 12px 16px;
    background:
        radial-gradient(ellipse at 10% 50%, {primary_faint} 0%, transparent 70%),
        #fff;
    border-radius: 4px;
    border-left: 3px solid {stroke_mid};
    font-style: italic;
}}

/* ── Certifications ─────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 0 4px 18px;
    font-size: 10pt;
    position: relative;
}}

.cert-list li::before {{
    content: "●";
    position: absolute;
    left: 0;
    color: {stroke_mid};
    font-size: 8pt;
    top: 6px;
}}

/* ── Page-break safety ──────────────────────────────────────── */

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
