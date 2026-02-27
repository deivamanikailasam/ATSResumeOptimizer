"""Aurora Borealis – Ethereal northern-lights-inspired design with a dramatic
multi-colour gradient header, soft glow accents, and an otherworldly palette."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "aurora_borealis",
    "name": "Aurora Borealis",
    "description": "Northern lights gradient header with ethereal glow accents",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.30)
    aurora_mid = lighten(primary_color, 0.40)
    shimmer = lighten(primary_color, 0.85)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 0;
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
    color: #1e1e2f;
    background: #fafaff;
}}

/* ── Aurora header ─────────────────────────────────────────── */

.resume-header {{
    background: linear-gradient(
        135deg,
        {primary_dark} 0%,
        {primary_color} 30%,
        {aurora_mid} 60%,
        {primary_light} 100%
    );
    color: #fff;
    padding: 34px 34px 28px;
    position: relative;
    overflow: hidden;
}}

.resume-header::before {{
    content: "";
    position: absolute;
    top: -60px;
    left: -40px;
    width: 280px;
    height: 280px;
    background: radial-gradient(circle, rgba(255,255,255,0.10) 0%, transparent 70%);
    border-radius: 50%;
}}

.resume-header::after {{
    content: "";
    position: absolute;
    bottom: -30px;
    right: 10%;
    width: 200px;
    height: 120px;
    background: radial-gradient(ellipse, rgba(255,255,255,0.08) 0%, transparent 70%);
    border-radius: 50%;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 300;
    color: #fff;
    letter-spacing: 2px;
    margin-bottom: 8px;
    position: relative;
    z-index: 1;
    text-shadow: 0 1px 8px rgba(0,0,0,0.15);
}}

.contact-info {{
    position: relative;
    z-index: 1;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: rgba(255,255,255,0.88);
    font-weight: 300;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: rgba(255,255,255,0.35);
}}

/* ── Shimmer accent bar ────────────────────────────────────── */

.resume-section:first-of-type {{
    margin-top: 0;
    border-top: 3px solid transparent;
    border-image: linear-gradient(
        90deg,
        {primary_color},
        {aurora_mid},
        {primary_light},
        {aurora_mid},
        {primary_color}
    ) 1;
}}

/* ── Sections ──────────────────────────────────────────────── */

.resume-section {{
    margin: 0 30px 14px;
    padding-top: 12px;
}}

.resume-section h2 {{
    font-size: 9pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2.5px;
    color: {primary_color};
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid {shimmer};
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
    font-weight: 600;
    color: #1e1e2f;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {aurora_mid};
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

li::marker {{
    color: {aurora_mid};
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
    margin-bottom: 2px;
}}

.skill-tag {{
    display: inline-block;
    background: linear-gradient(135deg, {primary_light}, {shimmer});
    color: {primary_dark};
    padding: 2px 10px;
    border-radius: 12px;
    margin: 2px 3px 2px 0;
    font-size: 8.5pt;
    font-weight: 600;
    border: none;
}}

/* ── Experience / Education / Projects ──────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
    padding-left: 12px;
    border-left: 2px solid {shimmer};
}}

.summary p {{
    font-size: 10pt;
    color: #444;
    line-height: 1.65;
    padding: 10px 16px;
    background: linear-gradient(135deg, {primary_light}88, #fff);
    border-radius: 6px;
}}

/* ── Certifications ─────────────────────────────────────────── */

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
    content: "✦";
    position: absolute;
    left: 0;
    color: {aurora_mid};
    font-size: 7pt;
    top: 7px;
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
