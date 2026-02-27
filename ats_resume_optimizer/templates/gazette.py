"""Gazette – Newspaper editorial layout with newsprint aesthetic."""

TEMPLATE = {
    "id": "gazette",
    "name": "Gazette",
    "description": "Newspaper editorial layout with classic newsprint column aesthetic",
}


def _render(content_html: str, primary_color: str) -> str:
    headline = "#1a1a1a"
    newsprint = "#faf9f6"
    column_rule = "#c0bcb4"
    byline = "#555550"
    dateline = "#777770"
    rule_thick = "#2a2a2a"
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
    font-family: 'Georgia', 'Times New Roman', 'Palatino Linotype', serif;
    font-size: 10pt;
    line-height: 1.5;
    color: {headline};
    background: {newsprint};
}}

/* ── Masthead / Header ──────────────────────────────────────── */

.resume-header {{
    text-align: center;
    padding: 10px 0 12px;
    margin-bottom: 14px;
    border-top: 4px double {rule_thick};
    border-bottom: 2px solid {rule_thick};
    position: relative;
}}

.resume-header::before {{
    content: "";
    display: block;
    height: 1px;
    background: {rule_thick};
    margin-bottom: 10px;
}}

.resume-header h1 {{
    font-size: 32pt;
    font-weight: 900;
    color: {headline};
    letter-spacing: -0.5px;
    margin-bottom: 4px;
    font-family: 'Georgia', 'Times New Roman', serif;
}}

.contact-info {{
    margin-top: 4px;
}}

.contact-info span {{
    font-size: 8.5pt;
    color: {dateline};
    font-style: italic;
}}

.contact-info span:not(:last-child)::after {{
    content: "  ◆  ";
    color: {column_rule};
    font-size: 5pt;
    font-style: normal;
    vertical-align: middle;
}}

/* ── Sections ───────────────────────────────────────────────── */

.resume-section {{
    margin-bottom: 12px;
    padding-top: 2px;
}}

.resume-section h2 {{
    font-size: 10pt;
    font-weight: 700;
    color: {headline};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 6px;
    padding: 3px 0;
    border-top: 2px solid {headline};
    border-bottom: 1px solid {headline};
    text-align: center;
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
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
    color: {headline};
    font-style: italic;
}}

.item-header .date {{
    float: right;
    font-size: 8.5pt;
    color: {dateline};
    font-weight: 400;
    white-space: nowrap;
    font-style: italic;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.company {{
    font-size: 9pt;
    color: {byline};
    margin-bottom: 3px;
    clear: both;
    font-variant: small-caps;
    letter-spacing: 0.5px;
}}

ul {{
    padding-left: 16px;
    margin-top: 3px;
}}

li {{
    font-size: 9.5pt;
    margin-bottom: 2px;
    color: #2a2a2a;
    text-align: justify;
}}

li::marker {{
    color: {primary_color};
}}

/* ── Skills ──────────────────────────────────────────────────── */

.skills-grid {{
    display: block;
    column-count: 2;
    column-gap: 16px;
    column-rule: 1px solid {column_rule};
}}

.skill-category {{
    margin-bottom: 6px;
    font-size: 9.5pt;
    break-inside: avoid;
}}

.skill-category strong {{
    color: {headline};
    display: block;
    margin-bottom: 2px;
    font-variant: small-caps;
    font-size: 10pt;
}}

.skill-tag {{
    display: inline;
    background: transparent;
    color: {byline};
    font-size: 9pt;
}}

.skill-tag:not(:last-child)::after {{
    content: ",  ";
}}

/* ── Experience / Education / Projects ───────────────────────── */

.experience-item,
.education-item,
.project-item {{
    margin-bottom: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid {column_rule};
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
    color: {byline};
    text-align: justify;
    font-style: italic;
}}

/* ── Certifications ──────────────────────────────────────────── */

.cert-list {{
    list-style: none;
    padding: 0;
    column-count: 2;
    column-gap: 16px;
    column-rule: 1px solid {column_rule};
}}

.cert-list li {{
    padding: 2px 0;
    font-size: 9.5pt;
    break-inside: avoid;
}}

.cert-list li::before {{
    content: "▸ ";
    color: {primary_color};
    font-size: 8pt;
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
