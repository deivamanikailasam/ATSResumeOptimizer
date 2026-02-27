"""Warm Timber – Rich warm wood-inspired tones with cream content areas."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "rosewood",
    "name": "Warm Timber",
    "description": "Rich warm wood-inspired tones with cream content areas and classic serif",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.7)
    primary_dark = darken(primary_color, 0.3)
    cream = "#fdf8f4"
    warm_cream = "#f5ede6"
    linen = "#eee5db"
    dark_text = "#2e1a1e"
    muted = "#7a5c60"
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
    font-family: 'Cambria', 'Georgia', 'Palatino Linotype', serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {dark_text};
    background: {cream};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    padding: 16px 20px;
    margin-bottom: 18px;
    background: {primary_dark};
    border-radius: 2px;
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 700;
    color: {cream};
    letter-spacing: 2px;
    margin-bottom: 5px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {primary_light};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ―  ";
    color: {primary_color};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding: 10px 14px;
    background: {warm_cream};
    border-radius: 3px;
    border-top: 3px solid {primary_color};
}}

.resume-section h2 {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px solid {linen};
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
    color: {primary_dark};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
    font-style: italic;
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
    color: #3e2a2e;
}}

li::marker {{
    color: {primary_light};
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
    color: {primary_dark};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_light};
    color: {primary_color};
    padding: 2px 10px;
    border-radius: 3px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-left: 12px;
    border-left: 2px solid {linen};
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: {muted};
    font-style: italic;
    padding: 6px 0;
    border-top: 1px solid {linen};
    border-bottom: 1px solid {linen};
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 4px 0;
    font-size: 10pt;
    border-bottom: 1px solid {linen};
}}

.cert-list li::before {{
    content: "◈ ";
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
