"""Neon Glass – Glassmorphism-inspired design with frosted header and subtle glow accents."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "neon_glass",
    "name": "Neon Glass",
    "description": "Glassmorphism-inspired frosted header with subtle glow accents",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.93)
    primary_muted = lighten(primary_color, 0.80)
    primary_dark = darken(primary_color, 0.30)
    glow_soft = lighten(primary_color, 0.60)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 10mm 0;
}}
@page :first {{
    margin-top: 0;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #1a1a2e;
    background: #fafbfc;
}}

/* ── Header (frosted glass) ─────────────────────────────────── */

.resume-header {{
    background: linear-gradient(135deg, {primary_color}dd, {primary_dark}cc);
    backdrop-filter: blur(12px);
    color: #fff;
    padding: 30px 32px 24px;
    position: relative;
    overflow: hidden;
}}

.resume-header::before {{
    content: "";
    position: absolute;
    top: -40px;
    right: -40px;
    width: 160px;
    height: 160px;
    background: rgba(255,255,255,0.08);
    border-radius: 50%;
}}

.resume-header::after {{
    content: "";
    position: absolute;
    bottom: -20px;
    left: 30%;
    width: 200px;
    height: 80px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 700;
    color: #fff;
    margin-bottom: 6px;
    position: relative;
    z-index: 1;
}}

.contact-info {{
    position: relative;
    z-index: 1;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: rgba(255,255,255,0.85);
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: rgba(255,255,255,0.4);
}}

/* ── Body padding ───────────────────────────────────────────── */

.resume-section {{
    margin: 0 28px 14px;
}}

.resume-section:first-of-type {{
    margin-top: 22px;
}}

.resume-section h2 {{
    font-size: 9.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {primary_color};
    margin-bottom: 8px;
    padding: 4px 12px;
    background: {primary_light};
    border-left: 3px solid {primary_color};
    border-radius: 0 4px 4px 0;
    display: inline-block;
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
    color: #1a1a2e;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
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

/* ── Skills ──────────────────────────────────────────────────── */

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
}}

.skill-tag {{
    display: inline-block;
    background: #fff;
    color: {primary_dark};
    padding: 2px 10px;
    border-radius: 14px;
    margin: 2px 3px 2px 0;
    font-size: 8.5pt;
    font-weight: 600;
    border: 1px solid {primary_muted};
    box-shadow: 0 1px 3px {glow_soft}44;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
    padding: 8px 12px;
    border-radius: 6px;
    background: #fff;
    border: 1px solid {primary_light};
}}

.summary p {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
    padding: 10px 14px;
    background: #fff;
    border-radius: 6px;
    border: 1px solid {primary_light};
    box-shadow: 0 1px 4px {glow_soft}22;
}}

/* ── Certifications ──────────────────────────────────────────── */

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
    color: {primary_color};
    font-size: 7pt;
    top: 7px;
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
