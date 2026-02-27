"""Terracotta – Warm Mediterranean-inspired design with earthy clay tones,
organic rounded corners, and a hand-crafted artisanal feel."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "terracotta",
    "name": "Terracotta",
    "description": "Warm earthy Mediterranean tones with organic rounded styling",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.91)
    primary_soft = lighten(primary_color, 0.82)
    primary_dark = darken(primary_color, 0.25)
    warm_bg = lighten(primary_color, 0.96)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 10mm 14mm;
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
    color: #2c2420;
    background: {warm_bg};
}}

/* ── Header ────────────────────────────────────────────────── */

.resume-header {{
    background: {primary_color};
    color: #fff;
    padding: 26px 28px 22px;
    border-radius: 12px 12px 0 0;
    position: relative;
}}

.resume-header::after {{
    content: "";
    display: block;
    position: absolute;
    bottom: -8px;
    left: 20px;
    right: 20px;
    height: 8px;
    background: linear-gradient(to bottom, {primary_dark}33, transparent);
    border-radius: 0 0 50% 50%;
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: #fff;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: rgba(255,255,255,0.85);
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: rgba(255,255,255,0.40);
}}

/* ── Sections ──────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding: 14px 20px;
    background: #fff;
    border-radius: 8px;
    border: 1px solid {primary_soft};
}}

.resume-section h2 {{
    font-size: 10pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {primary_color};
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 2px solid {primary_light};
    display: flex;
    align-items: center;
}}

.resume-section h2::before {{
    content: "";
    display: inline-block;
    width: 6px;
    height: 6px;
    background: {primary_color};
    border-radius: 50%;
    margin-right: 8px;
    flex-shrink: 0;
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
    color: #2c2420;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
    background: {primary_light};
    padding: 1px 8px;
    border-radius: 10px;
}}

.company {{
    font-size: 9.5pt;
    color: #665;
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 16px;
    margin-top: 4px;
}}

li {{
    font-size: 10pt;
    margin-bottom: 2px;
    color: #3a3330;
}}

li::marker {{
    color: {primary_color};
}}

/* ── Skills ─────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 8px;
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
    background: {primary_light};
    color: {primary_dark};
    padding: 3px 10px;
    border-radius: 14px;
    margin: 2px 4px 2px 0;
    font-size: 8.5pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ──────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 14px;
    page-break-inside: avoid;
    padding: 10px 14px;
    background: {warm_bg};
    border-radius: 8px;
    border-left: 3px solid {primary_soft};
}}

.summary p {{
    font-size: 10pt;
    color: #3a3330;
    line-height: 1.65;
    padding: 10px 14px;
    background: {warm_bg};
    border-radius: 8px;
    border-left: 3px solid {primary_color};
}}

/* ── Certifications ─────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 5px 10px;
    font-size: 10pt;
    margin-bottom: 4px;
    background: {primary_light};
    border-radius: 6px;
    display: inline-block;
    margin-right: 6px;
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
