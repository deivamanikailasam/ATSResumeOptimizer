"""Paper Cut – Layered depth via box-shadows, paper cut-out card-style sections."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "paper_cut",
    "name": "Paper Cut",
    "description": "Layered paper depth with shadow effects and card-style sections",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.2)
    paper = "#ffffff"
    canvas = "#edeae5"
    shadow_color = "rgba(0,0,0,0.08)"
    shadow_deep = "rgba(0,0,0,0.12)"
    charcoal = "#2a2a2a"
    gray = "#666660"
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
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {charcoal};
    background: {canvas};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    background: {paper};
    padding: 20px 22px 16px;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px {shadow_deep}, 0 1px 3px {shadow_color};
    border-bottom: 3px solid {primary_color};
    position: relative;
}}

.resume-header::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: {primary_color};
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: {charcoal};
    margin-bottom: 5px;
    padding-left: 10px;
}}

.contact-info {{
    padding-left: 10px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {gray};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ·  ";
    color: #bbb;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    background: {paper};
    margin-bottom: 10px;
    padding: 12px 16px;
    box-shadow: 0 2px 6px {shadow_color}, 0 1px 2px {shadow_color};
    position: relative;
}}

.resume-section::before {{
    content: "";
    position: absolute;
    bottom: -3px;
    left: 4px;
    right: 4px;
    height: 3px;
    background: {canvas};
    box-shadow: 0 2px 4px {shadow_color};
    z-index: -1;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 700;
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
    color: {charcoal};
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
    color: {gray};
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
    color: #444;
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
    color: {charcoal};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {paper};
    color: {primary_dark};
    padding: 2px 9px;
    margin: 2px 3px 2px 0;
    font-size: 9pt;
    font-weight: 600;
    box-shadow: 0 1px 3px {shadow_color};
    border-radius: 2px;
    border: 1px solid #e8e5e0;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px dashed #ddd;
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
    color: #555;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 8px;
    font-size: 10pt;
    margin-bottom: 4px;
    background: {primary_light};
    border-radius: 2px;
    box-shadow: 0 1px 2px {shadow_color};
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
