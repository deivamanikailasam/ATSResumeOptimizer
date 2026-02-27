"""Sidebar Pro – Two-column layout with a bold colored sidebar for contact and skills."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "sidebar_pro",
    "name": "Sidebar Pro",
    "description": "Two-column layout with colored sidebar for contact and skills",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.93)
    primary_dark = darken(primary_color, 0.30)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: A4;
    margin: 10mm 0;
}}
@page :first {{
    margin-top: 0;
}}

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #1a1a1a;
}}

/* ── Two-column grid ────────────────────────────────────────── */

.resume-container {{
    display: grid;
    grid-template-columns: 230px 1fr;
    grid-template-rows: auto auto auto auto auto;
    min-height: 100vh;
    position: relative;
}}

.resume-container::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 230px;
    bottom: 0;
    background: {primary_color};
    z-index: 0;
}}

.resume-container > * {{
    position: relative;
    z-index: 1;
}}

/* ── Sidebar column (header, skills, certs) ─────────────────── */

.resume-header {{
    grid-column: 1;
    grid-row: 1;
    background: {primary_dark};
    color: #fff;
    padding: 28px 20px 18px;
    text-align: center;
}}

.resume-header h1 {{
    font-size: 18pt;
    font-weight: 800;
    color: #fff;
    margin-bottom: 10px;
    letter-spacing: 0.5px;
}}

.contact-info {{
    display: flex;
    flex-direction: column;
    gap: 3px;
}}

.contact-info span {{
    font-size: 8pt;
    color: {primary_light};
    word-break: break-all;
}}

.resume-section.skills {{
    grid-column: 1;
    grid-row: 2 / 4;
    background: {primary_color};
    color: #fff;
    padding: 14px 20px 12px;
}}

.resume-section.certifications {{
    grid-column: 1;
    grid-row: 4 / 6;
    background: {primary_color};
    color: #fff;
    padding: 14px 20px 12px;
}}

.resume-section.skills h2,
.resume-section.certifications h2 {{
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #fff;
    border-bottom: 1px solid rgba(255,255,255,0.3);
    padding-bottom: 5px;
    margin-bottom: 10px;
}}

.skills-grid {{
    display: block;
}}

.skill-category {{
    margin-bottom: 8px;
    font-size: 9pt;
}}

.skill-category strong {{
    color: #fff;
    font-size: 8.5pt;
    display: block;
    margin-bottom: 3px;
    opacity: 0.85;
}}

.skill-tag {{
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: #fff;
    padding: 2px 7px;
    border-radius: 3px;
    margin: 1px 3px 2px 0;
    font-size: 8pt;
    font-weight: 500;
}}

.cert-list {{
    list-style: none;
    padding: 0;
}}

.cert-list li {{
    font-size: 8.5pt;
    padding: 4px 0;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    color: #fff;
}}

.cert-list li:last-child {{
    border-bottom: none;
}}

/* ── Main column (summary, experience, education, projects) ── */

.resume-section.summary {{
    grid-column: 2;
    grid-row: 1;
    padding: 24px 28px 10px;
    margin-bottom: 0;
}}

.resume-section.experience {{
    grid-column: 2;
    grid-row: 2 / 4;
    padding: 10px 28px;
}}

.resume-section.education {{
    grid-column: 2;
    grid-row: 4;
    padding: 10px 28px;
}}

.resume-section.projects {{
    grid-column: 2;
    grid-row: 5;
    padding: 10px 28px;
}}

.resume-section h2 {{
    font-size: 10pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {primary_color};
    padding-bottom: 4px;
    margin-bottom: 8px;
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
    font-weight: 700;
    color: #111;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {primary_color};
    font-weight: 600;
    white-space: nowrap;
}}

.company {{
    font-size: 9.5pt;
    color: #666;
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
    color: #333;
}}

.summary p {{
    font-size: 10pt;
    color: #444;
    line-height: 1.6;
}}

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 12px;
    page-break-inside: avoid;
}}

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
