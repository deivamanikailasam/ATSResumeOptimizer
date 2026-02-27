"""Obsidian Prestige – Luxury dark charcoal with elegant accents, executive prestige."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "obsidian_gold",
    "name": "Obsidian Prestige",
    "description": "Luxury dark charcoal background with elegant accent lines, executive prestige",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.90)
    primary_dark = darken(primary_color, 0.25)
    charcoal = "#1e1e1e"
    charcoal_mid = "#2a2a2a"
    off_white = "#f0ece2"
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
    font-family: 'Georgia', 'Garamond', 'Times New Roman', serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {off_white};
    background: {charcoal};
}}

.resume-container {{
    background: {charcoal};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 22px 20px 16px;
    margin-bottom: 18px;
    border-top: 3px solid {primary_color};
    border-bottom: 3px solid {primary_color};
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 700;
    color: {primary_color};
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {primary_light};
    letter-spacing: 0.5px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ◆  ";
    color: {primary_color};
    font-size: 6pt;
    vertical-align: middle;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding: 10px 14px;
    background: {charcoal_mid};
    border-left: 3px solid {primary_color};
    border-radius: 2px;
}}

.resume-section h2 {{
    font-size: 11pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid {primary_dark};
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
    color: {off_white};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_light};
    font-weight: 600;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #b0a88e;
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
    color: #d5d0c4;
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
    color: {primary_light};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {charcoal};
    color: {primary_color};
    padding: 2px 10px;
    border: 1px solid {primary_dark};
    border-radius: 2px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 600;
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 10pt;
    color: #d5d0c4;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    border-bottom: 1px solid {primary_dark};
    color: #d5d0c4;
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
