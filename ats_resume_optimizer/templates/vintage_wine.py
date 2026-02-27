"""Vintage Charm – Classic vintage aesthetic with aged parchment warmth and timeless charm."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "vintage_wine",
    "name": "Vintage Charm",
    "description": "Classic vintage aesthetic with aged parchment warmth and timeless charm",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_dark = darken(primary_color, 0.25)
    parchment = "#f8f3eb"
    aged = "#e8dfd2"
    cork = "#a89278"
    vintage_text = "#2e1f1a"
    label_cream = "#f0e8da"
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
    font-family: 'Garamond', 'Georgia', 'Palatino Linotype', serif;
    font-size: 10pt;
    line-height: 1.55;
    color: {vintage_text};
    background: {parchment};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 18px 20px 14px;
    margin-bottom: 18px;
    border: 2px solid {primary_color};
    position: relative;
}}

.resume-header::before,
.resume-header::after {{
    content: "";
    position: absolute;
    width: 12px;
    height: 12px;
    border: 2px solid {primary_color};
}}

.resume-header::before {{
    top: -2px;
    left: -2px;
    border-right: none;
    border-bottom: none;
}}

.resume-header::after {{
    bottom: -2px;
    right: -2px;
    border-left: none;
    border-top: none;
}}

.resume-header h1 {{
    font-size: 28pt;
    font-weight: 400;
    color: {primary_dark};
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {cork};
    letter-spacing: 0.3px;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ⸱  ";
    color: {primary_color};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    padding: 4px 0;
    text-align: center;
    position: relative;
}}

.resume-section h2::before {{
    content: "~ ";
    color: {cork};
}}

.resume-section h2::after {{
    content: " ~";
    color: {cork};
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
    font-weight: 400;
    white-space: nowrap;
    font-style: italic;
}}

.company {{
    font-size: 9.5pt;
    color: {cork};
    margin-bottom: 3px;
    clear: both;
    font-style: italic;
}}

ul {{
    padding-left: 16px;
    margin-top: 3px;
}}

li {{
    font-size: 10pt;
    margin-bottom: 2px;
    color: {vintage_text};
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
    color: {primary_dark};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {label_cream};
    color: {primary_dark};
    padding: 2px 10px;
    border: 1px solid {aged};
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
    padding-bottom: 8px;
    border-bottom: 1px solid {aged};
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
    color: {cork};
    text-align: center;
    font-style: italic;
    padding: 8px 20px;
    background: {label_cream};
    border: 1px solid {aged};
    border-radius: 2px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
    text-align: center;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    display: inline-block;
    margin: 2px 8px;
}}

.cert-list li::before {{
    content: "❧ ";
    color: {primary_color};
    font-size: 9pt;
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
