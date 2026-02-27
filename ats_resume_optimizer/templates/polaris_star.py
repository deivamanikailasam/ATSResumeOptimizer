"""Polaris Star – Deep navy with celestial-inspired dotted motifs and starlight accents."""

from ._colors import lighten, darken, hex_to_rgb

TEMPLATE = {
    "id": "polaris_star",
    "name": "Polaris Star",
    "description": "Deep navy with celestial-inspired dotted motifs and starlight accents",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_dark = darken(primary_color, 0.3)
    r, g, b = hex_to_rgb(primary_dark)
    primary_dark_rgba = f"rgba({r},{g},{b}"
    navy = "#0f1b2d"
    navy_mid = "#1a2940"
    silver = "#b8c4d0"
    silver_bright = "#d8e0e8"
    starlight = "#e8ecf2"
    deep_text = "#e0e4ea"
    body_text = "#c8ced8"
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
    color: {body_text};
    background: {navy};
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 22px 20px 16px;
    margin-bottom: 18px;
    border-bottom: 1px dotted {primary_dark};
    position: relative;
}}

.resume-header::before {{
    content: "✦";
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    background: {navy};
    padding: 0 10px;
    color: {primary_color};
    font-size: 10pt;
}}

.resume-header h1 {{
    font-size: 26pt;
    font-weight: 300;
    color: {silver_bright};
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 6px;
}}

.contact-info span {{
    font-size: 9pt;
    color: {silver};
}}

.contact-info span:not(:last-child)::after {{
    content: "  ✦  ";
    color: {primary_color};
    font-size: 6pt;
    vertical-align: middle;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding: 10px 14px;
    background: {navy_mid};
    border-radius: 3px;
    border: 1px solid {primary_dark_rgba},0.2);
}}

.resume-section h2 {{
    font-size: 10.5pt;
    font-weight: 600;
    color: {primary_color};
    text-transform: uppercase;
    letter-spacing: 2.5px;
    margin-bottom: 8px;
    padding-bottom: 5px;
    border-bottom: 1px dotted {primary_dark};
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
    color: {deep_text};
}}

.item-header .date {{
    float: right;
    font-size: 9pt;
    color: {primary_dark};
    font-weight: 500;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: {silver};
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
    color: {body_text};
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
    color: {silver_bright};
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: {primary_dark_rgba},0.2);
    color: {starlight};
    padding: 2px 10px;
    border-radius: 3px;
    margin: 1px 3px 1px 0;
    font-size: 9pt;
    font-weight: 500;
    border: 1px solid {primary_dark_rgba},0.35);
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px dotted {primary_dark_rgba},0.3);
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
    color: {silver};
    text-align: center;
    font-style: italic;
    letter-spacing: 0.3px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 10pt;
    border-bottom: 1px dotted {primary_dark_rgba},0.3);
    color: {body_text};
}}

.cert-list li::before {{
    content: "★ ";
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
