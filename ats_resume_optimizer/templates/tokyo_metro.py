"""Tokyo Metro – Japanese minimalism with ultra-clean grid and thin accent lines."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "tokyo_metro",
    "name": "Tokyo Metro",
    "description": "Japanese minimalism — ultra-clean grid with thin accent lines",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.94)
    primary_muted = lighten(primary_color, 0.80)
    primary_dark = darken(primary_color, 0.20)
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
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.6;
    color: #2c2c2c;
    letter-spacing: 0.2px;
}}

/* ── Header ─────────────────────────────────────────────────── */

.resume-header {{
    border-top: 4px solid {primary_color};
    padding: 20px 0 14px;
    margin-bottom: 18px;
}}

.resume-header h1 {{
    font-size: 24pt;
    font-weight: 300;
    color: #111;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.contact-info {{
    display: flex;
    gap: 0;
    flex-wrap: wrap;
}}

.contact-info span {{
    font-size: 8pt;
    color: #777;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}}

.contact-info span:not(:last-child)::after {{
    content: "  |  ";
    color: {primary_muted};
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 16px;
    padding-left: 18px;
    position: relative;
}}

.resume-section::before {{
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: {primary_light};
}}

.resume-section h2 {{
    font-size: 8pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: {primary_color};
    margin-bottom: 10px;
    padding-bottom: 5px;
}}

/* ── Items ───────────────────────────────────────────────────── */

.item-header {{
    display: block;
    overflow: hidden;
    margin-bottom: 1px;
}}

.item-header h3 {{
    float: left;
    font-size: 10pt;
    font-weight: 600;
    color: #1a1a1a;
}}

.item-header .date {{
    float: right;
    font-size: 8pt;
    color: {primary_dark};
    font-weight: 400;
    white-space: nowrap;
    letter-spacing: 0.5px;
}}

.company {{
    font-size: 9pt;
    color: #888;
    margin-bottom: 3px;
    clear: both;
    letter-spacing: 0.5px;
}}

ul {{
    padding-left: 14px;
    margin-top: 3px;
}}

li {{
    font-size: 9.5pt;
    margin-bottom: 2px;
    color: #444;
}}

li::marker {{
    color: {primary_muted};
    font-size: 8pt;
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 6px;
    font-size: 9.5pt;
}}

.skill-category strong {{
    color: #555;
    font-size: 8pt;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    display: block;
    margin-bottom: 3px;
}}

.skill-tag {{
    display: inline-block;
    background: transparent;
    color: {primary_dark};
    padding: 1px 0;
    margin: 0 8px 1px 0;
    font-size: 9pt;
    font-weight: 500;
    border-bottom: 1px solid {primary_muted};
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

.summary p {{
    font-size: 9.5pt;
    color: #555;
    line-height: 1.65;
    border-left: 3px solid {primary_color};
    padding-left: 12px;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    padding: 3px 0;
    font-size: 9.5pt;
    color: #444;
    border-bottom: 1px solid {primary_light};
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
