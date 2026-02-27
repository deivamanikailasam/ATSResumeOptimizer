"""Carbon Fiber – Dark tech-luxury with subtle woven pattern, futuristic professional."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "carbon_fiber",
    "name": "Carbon Fiber",
    "description": "Dark tech-luxury with subtle woven carbon pattern, futuristic professional",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.85)
    primary_dark = darken(primary_color, 0.3)
    carbon = "#141414"
    carbon_mid = "#1e1e1e"
    carbon_light = "#2a2a2a"
    titanium = "#a0a8b0"
    chrome = "#d0d4d8"
    ghost = "#e8eaec"
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
    font-family: 'Consolas', 'SF Mono', 'Roboto Mono', monospace;
    font-size: 10pt;
    line-height: 1.55;
    color: {chrome};
    background: {carbon};
    background-image:
        linear-gradient(45deg, {carbon_mid} 25%, transparent 25%),
        linear-gradient(-45deg, {carbon_mid} 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, {carbon_mid} 75%),
        linear-gradient(-45deg, transparent 75%, {carbon_mid} 75%);
    background-size: 4px 4px;
    background-position: 0 0, 0 2px, 2px -2px, -2px 0px;
}}

.resume-container {{
    background: transparent;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 18px 20px 14px;
    margin-bottom: 16px;
    background: {carbon_light};
    border-bottom: 2px solid {primary_color};
    border-top: 1px solid #333;
    position: relative;
}}

.resume-header::after {{
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100px;
    height: 2px;
    background: {primary_color};
    box-shadow: 0 0 8px {primary_color};
}}

.resume-header h1 {{
    font-size: 24pt;
    font-weight: 700;
    color: {ghost};
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 5px;
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: {titanium};
}}

.contact-info span:not(:last-child)::after {{
    content: "  |  ";
    color: {primary_dark};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding: 10px 14px;
    background: rgba(30, 30, 30, 0.8);
    border-left: 2px solid {primary_color};
    border-radius: 2px;
}}

.resume-section h2 {{
    font-size: 9.5pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 3px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid #333;
    font-family: 'Consolas', 'SF Mono', monospace;
}}

.resume-section h2::before {{
    content: "// ";
    color: {primary_dark};
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
    color: {ghost};
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
    font-family: 'Consolas', monospace;
}}

.company {{
    font-size: 9pt;
    color: {titanium};
    margin-bottom: 3px;
    clear: both;
}}

ul {{
    padding-left: 16px;
    margin-top: 3px;
}}

li {{
    font-size: 9.5pt;
    margin-bottom: 2px;
    color: {chrome};
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
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
    color: {ghost};
    display: block;
    margin-bottom: 3px;
    font-family: 'Segoe UI', sans-serif;
}}

.skill-tag {{
    display: inline-block;
    background: {carbon};
    color: {primary_color};
    padding: 2px 9px;
    margin: 1px 3px 1px 0;
    font-size: 8.5pt;
    font-weight: 600;
    border: 1px solid {primary_dark};
    border-radius: 2px;
    font-family: 'Consolas', monospace;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid #2a2a2a;
    page-break-inside: avoid;
}}

.experience-item:last-child,
.education-item:last-child,
.project-item:last-child {{
    border-bottom: none;
    padding-bottom: 0;
}}

.summary p {{
    font-size: 9.5pt;
    color: {titanium};
    padding-left: 10px;
    border-left: 2px solid {primary_dark};
    font-family: 'Segoe UI', sans-serif;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 9.5pt;
    border-bottom: 1px solid #2a2a2a;
    color: {chrome};
    font-family: 'Segoe UI', sans-serif;
}}

.cert-list li::before {{
    content: "▹ ";
    color: {primary_color};
    font-size: 9pt;
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
