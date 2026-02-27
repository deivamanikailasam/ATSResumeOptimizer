"""Origami – Clean geometric folds, angular dividers inspired by paper folding."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "origami",
    "name": "Origami",
    "description": "Clean geometric folds and angular dividers inspired by paper folding art",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.2)
    paper_white = "#ffffff"
    crease = "#e0e4e8"
    shadow_fold = "#d0d5dc"
    deep = "#1c2a3a"
    mid = "#4a5a6a"
    soft_bg = "#f6f8fa"
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
    color: {deep};
    background: {soft_bg};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 18px 20px 14px;
    margin-bottom: 16px;
    background: {paper_white};
    position: relative;
    border-left: 4px solid {primary_color};
    box-shadow: 2px 2px 0 {crease};
}}

.resume-header::before {{
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 0 28px 28px 0;
    border-color: transparent {soft_bg} transparent transparent;
}}

.resume-header::after {{
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 28px 0 0 28px;
    border-color: transparent transparent transparent {shadow_fold};
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: {deep};
    letter-spacing: 1px;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {mid};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ▸  ";
    color: {primary_color};
    font-size: 8pt;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
    padding: 10px 14px;
    background: {paper_white};
    position: relative;
    box-shadow: 1px 1px 0 {crease};
}}

.resume-section::before {{
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 4px;
    height: 100%;
    background: {primary_color};
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 2px solid {crease};
    position: relative;
}}

.resume-section h2::after {{
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 0 0 8px 8px;
    border-color: transparent transparent {crease} transparent;
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
    color: {deep};
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
    color: {mid};
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
    color: #2c3a4a;
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
    color: {deep};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_dark};
    padding: 2px 9px;
    margin: 2px 3px 2px 0;
    font-size: 9pt;
    font-weight: 600;
    clip-path: polygon(6px 0%, 100% 0%, calc(100% - 6px) 100%, 0% 100%);
    padding-left: 12px;
    padding-right: 12px;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid {crease};
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
    color: {mid};
    padding: 8px 12px;
    background: {primary_light};
    border-left: 3px solid {primary_color};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0 3px 8px;
    font-size: 10pt;
    border-left: 2px solid {crease};
    margin-bottom: 4px;
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
