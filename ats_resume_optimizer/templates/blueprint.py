"""Blueprint – Technical/architectural drawing aesthetic with monospace accents,
dashed grid lines, and engineering-precision styling."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "blueprint",
    "name": "Blueprint",
    "description": "Technical drawing aesthetic with monospace accents and grid-line precision",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.25)
    grid_line = lighten(primary_color, 0.80)
    bg_tint = lighten(primary_color, 0.96)
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
    font-family: 'Consolas', 'Courier New', 'Lucida Console', monospace;
    font-size: 9.5pt;
    line-height: 1.55;
    color: #1a2a3a;
    background: {bg_tint};
}}

.resume-container {{
    border: 2px solid {primary_color};
    padding: 4px;
    background: #fff;
}}

.resume-container > * {{
    padding: 0 18px;
}}

/* ── Grid background effect ────────────────────────────────── */

.resume-container {{
    background-image:
        linear-gradient({grid_line}44 1px, transparent 1px),
        linear-gradient(90deg, {grid_line}44 1px, transparent 1px);
    background-size: 20px 20px;
    background-color: #fff;
}}

/* ── Header (title block) ──────────────────────────────────── */

.resume-header {{
    padding: 20px 18px 16px;
    border-bottom: 2px solid {primary_color};
    margin-bottom: 4px;
    position: relative;
    background: rgba(255,255,255,0.9);
}}

.resume-header::before {{
    content: "◁ RESUME ▷";
    position: absolute;
    top: 6px;
    right: 18px;
    font-size: 7pt;
    letter-spacing: 2px;
    color: {grid_line};
    font-family: 'Consolas', monospace;
}}

.resume-header h1 {{
    font-size: 22pt;
    font-weight: 700;
    color: {primary_dark};
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}}

.contact-info span {{
    font-size: 8pt;
    color: #556;
    font-family: 'Consolas', monospace;
}}

.contact-info span:not(:last-child)::after {{
    content: "  //  ";
    color: {grid_line};
}}

/* ── Sections ──────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 12px;
    padding-top: 10px;
    padding-bottom: 4px;
    border-top: 1px dashed {primary_color};
    background: rgba(255,255,255,0.85);
}}

.resume-section h2 {{
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: {primary_color};
    margin-bottom: 8px;
    font-family: 'Consolas', monospace;
    position: relative;
    display: inline-block;
    padding-right: 8px;
}}

.resume-section h2::before {{
    content: "// ";
    color: {grid_line};
}}

/* ── Items ──────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 2px;
}}

.item-header h3 {{
    float: left;
    font-size: 10pt;
    font-weight: 700;
    color: {primary_dark};
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}}

.item-header .date {{
    float: right;
    font-size: 8pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
    font-family: 'Consolas', monospace;
    padding: 1px 6px;
    border: 1px dashed {grid_line};
}}

.company {{
    font-size: 9pt;
    color: #556;
    margin-bottom: 3px;
    clear: both;
    font-family: 'Consolas', monospace;
}}

ul {{
    padding-left: 20px;
    margin-top: 4px;
    list-style: none;
}}

li {{
    font-size: 9.5pt;
    margin-bottom: 2px;
    color: #2a3a4a;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
    position: relative;
    padding-left: 2px;
}}

li::before {{
    content: "▸ ";
    color: {primary_color};
    font-size: 8pt;
    position: absolute;
    left: -14px;
    top: 1px;
}}

/* ── Skills ─────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 6px;
    font-size: 9.5pt;
}}

.skill-category strong {{
    color: {primary_dark};
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    display: block;
    margin-bottom: 2px;
    font-family: 'Consolas', monospace;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 1px 8px;
    margin: 2px 3px 2px 0;
    font-size: 8.5pt;
    font-weight: 600;
    border: 1px solid {grid_line};
    font-family: 'Consolas', monospace;
    letter-spacing: 0.3px;
}}

/* ── Experience / Education / Projects ──────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
    padding-bottom: 8px;
    border-bottom: 1px dashed {grid_line};
}}

.experience-item:last-child,
.education-item:last-child,
.project-item:last-child {{
    border-bottom: none;
}}

.summary p {{
    font-size: 9.5pt;
    color: #2a3a4a;
    line-height: 1.6;
    padding: 8px 12px;
    background: {primary_light};
    border: 1px dashed {grid_line};
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}}

/* ── Certifications ─────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 9.5pt;
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
}}

.cert-list li::before {{
    content: "[✓] ";
    color: {primary_color};
    font-family: 'Consolas', monospace;
    font-size: 8pt;
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
