"""Tech Professional – Developer-centric design with colored headers and tag pills."""

from ._colors import lighten

TEMPLATE = {
    "id": "tech_professional",
    "name": "Tech Professional",
    "description": "Developer-focused layout with colored header bars and skill pills",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
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
    line-height: 1.45;
    color: #24292e;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 3px solid {primary_color};
}}

.resume-header h1 {{
    font-size: 24pt;
    font-weight: 700;
    color: #24292e;
    margin-bottom: 4px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: #586069;
    font-family: Consolas, 'Courier New', monospace;
}}

.contact-info span:not(:last-child)::after {{
    content: "  //  ";
    color: #bbb;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 14px;
}}

.resume-section h2 {{
    font-size: 9.5pt;
    font-weight: 700;
    color: #fff;
    background-color: {primary_color};
    padding: 4px 10px;
    margin-bottom: 9px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
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
    color: #24292e;
}}

.item-header .date {{
    float: right;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 8.5pt;
    color: #586069;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #444d56;
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
    color: #24292e;
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
    color: #24292e;
    display: block;
    margin-bottom: 3px;
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.skill-tag {{
    display: inline-block;
    border: 1px solid {primary_color};
    color: {primary_color};
    padding: 1px 8px;
    border-radius: 12px;
    margin: 1px 3px 1px 0;
    font-size: 8.5pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 11px;
    padding-left: 8px;
    border-left: 2px solid {primary_light};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #24292e;
    padding: 6px 10px;
    background: {primary_light};
    border-left: 3px solid {primary_color};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0 3px 14px;
    font-size: 10pt;
    position: relative;
}}

.cert-list li::before {{
    content: "▸";
    position: absolute;
    left: 0;
    color: {primary_color};
    font-size: 10pt;
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
