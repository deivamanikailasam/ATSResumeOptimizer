# Template System

This guide covers how the template system works, how to customize existing templates, and how to author new ones.

## Overview

ATS Resume Optimizer separates **content** from **presentation**. The AI generates resume content as semantic HTML with standardized class names. Each template is a standalone Python module that wraps that content in a fully styled HTML document.

```
AI Output (content HTML)  ──►  Template Render  ──►  Full HTML Document  ──►  PDF
      ↑                              ↑
 CONTENT_STRUCTURE              Theme CSS +
 defines the contract           primary_color
```

This means:

- Any template can render any AI-generated resume.
- Changing the template does not require re-running the AI.
- New templates can be added without modifying any other code.

## Content Structure Contract

All templates must style the following HTML structure, defined in `CONTENT_STRUCTURE` (`templates/__init__.py`):

```html
<!-- Header with name and contact info -->
<div class="resume-header">
    <h1>FULL NAME</h1>
    <div class="contact-info">
        <span>email</span>
        <span>phone</span>
        <span>location</span>
        <span>linkedin</span>
    </div>
</div>

<!-- Professional Summary -->
<div class="resume-section summary">
    <h2>Professional Summary</h2>
    <p>Summary text.</p>
</div>

<!-- Skills Grid -->
<div class="resume-section skills">
    <h2>Technical Skills</h2>
    <div class="skills-grid">
        <div class="skill-category">
            <strong>Category:</strong>
            <span class="skill-tag">Skill</span>
        </div>
    </div>
</div>

<!-- Experience -->
<div class="resume-section experience">
    <h2>Professional Experience</h2>
    <div class="experience-item">
        <div class="item-header">
            <h3>Job Title</h3>
            <span class="date">Date Range</span>
        </div>
        <div class="company">Company · Location</div>
        <ul>
            <li>Achievement bullet.</li>
        </ul>
    </div>
</div>

<!-- Education -->
<div class="resume-section education">
    <h2>Education</h2>
    <div class="education-item">
        <div class="item-header">
            <h3>Degree</h3>
            <span class="date">Date Range</span>
        </div>
        <div class="company">University · Location</div>
    </div>
</div>

<!-- Projects (optional) -->
<div class="resume-section projects">
    <h2>Notable Projects</h2>
    <div class="project-item">
        <div class="item-header">
            <h3>Project Name</h3>
            <span class="date">Year</span>
        </div>
        <p>Description.</p>
    </div>
</div>

<!-- Certifications (optional) -->
<div class="resume-section certifications">
    <h2>Certifications</h2>
    <ul class="cert-list">
        <li><strong>Cert Name</strong> – Issuer (Year)</li>
    </ul>
</div>
```

### CSS Class Reference

| Class | Element | Description |
|---|---|---|
| `.resume-header` | `div` | Top section with name and contact |
| `.contact-info` | `div` | Container for contact `<span>` elements |
| `.resume-section` | `div` | Generic section wrapper |
| `.summary` | modifier | Applied alongside `.resume-section` for the summary |
| `.skills` | modifier | Applied alongside `.resume-section` for skills |
| `.experience` | modifier | Applied alongside `.resume-section` for experience |
| `.education` | modifier | Applied alongside `.resume-section` for education |
| `.projects` | modifier | Applied alongside `.resume-section` for projects |
| `.certifications` | modifier | Applied alongside `.resume-section` for certifications |
| `.skills-grid` | `div` | Container for skill categories |
| `.skill-category` | `div` | One category of skills |
| `.skill-tag` | `span` | Individual skill label |
| `.experience-item` | `div` | One job entry |
| `.education-item` | `div` | One education entry |
| `.project-item` | `div` | One project entry |
| `.item-header` | `div` | Title + date row within an item |
| `.date` | `span` | Date range, inside `.item-header` |
| `.company` | `div` | Company/university name and location |
| `.cert-list` | `ul` | Certification list |

## Template Module Structure

Every template module must:

1. **Export a `TEMPLATE` dict** with `id`, `name`, and `description`.
2. **Define a `_render(content_html, primary_color)` function** that returns a complete HTML document.
3. **Assign the render function**: `TEMPLATE["render"] = _render`.

### Minimal Example

```python
"""My Custom Theme – Short description of the visual style."""

from ._colors import lighten, darken

TEMPLATE = {
    "id": "my_custom_theme",
    "name": "My Custom Theme",
    "description": "Brief description of the visual style and character",
}


def _render(content_html: str, primary_color: str) -> str:
    primary_light = lighten(primary_color, 0.92)
    primary_dark = darken(primary_color, 0.2)

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
    font-family: 'Segoe UI', Roboto, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #2d2d2d;
}}

/* Style all the content structure classes here */

.resume-header h1 {{
    color: {primary_color};
}}

/* ... more CSS targeting the content structure classes ... */

</style>
</head>
<body>
{content_html}
</body>
</html>"""


TEMPLATE["render"] = _render
```

## Creating a New Template

### Step 1: Create the Module

Create a new file at `ats_resume_optimizer/templates/your_theme.py`.

### Step 2: Implement the Template

Follow the module structure above. Key guidelines:

- **Use `@page` rules** to set A4 size and margins.
- **Reset box model** with `*, *::before, *::after { box-sizing: border-box; }`.
- **Use `primary_color`** for accents — headings, borders, backgrounds.
- **Derive color variants** using `lighten()` and `darken()` from `_colors.py`.
- **Use CSS `f-string` formatting** — double all braces (`{{`, `}}`) in CSS.
- **Add `page-break-inside: avoid`** to experience/education/project items.
- **Add `page-break-after: avoid`** to headings.
- **Style all content structure classes** — the AI may produce any of the sections.

### Step 3: Register the Template

In `ats_resume_optimizer/templates/__init__.py`:

1. Add the import:

   ```python
   from .your_theme import TEMPLATE as your_theme
   ```

2. Add to the `TEMPLATES` OrderedDict:

   ```python
   TEMPLATES = OrderedDict([
       # ... existing entries ...
       ("your_theme", your_theme),
   ])
   ```

The template will automatically appear in the Streamlit dropdown and CLI `--template` choices.

## Color Utilities

The `_colors.py` module provides helpers for deriving color variants:

```python
from ._colors import hex_to_rgb, rgb_to_hex, lighten, darken

lighten("#2563eb", 0.92)   # Very light tint for backgrounds
lighten("#2563eb", 0.5)    # Medium tint
darken("#2563eb", 0.3)     # Darker shade for borders/text
```

| Function | Behavior |
|---|---|
| `lighten(color, factor)` | Blends toward `#ffffff`. `0.0` = original, `1.0` = white. |
| `darken(color, factor)` | Scales toward `#000000`. `0.0` = original, `1.0` = black. |

## Print and PDF Considerations

Templates render inside headless Chromium for PDF export. Keep these in mind:

- **All CSS features are supported** — flexbox, grid, pseudo-elements, gradients, etc.
- **Web fonts are not loaded** — use system font stacks (`'Segoe UI', Roboto, Arial, sans-serif`).
- **`print_background: True`** is enabled — background colors and images will appear in the PDF.
- **Page breaks** — use `page-break-inside: avoid` on items and `page-break-after: avoid` on headings. Additional page-break CSS is injected by `pdf_export.py` as a safety net.
- **Target 1–2 pages** — use compact spacing. The `@page` margin controls the physical margins.

## Testing a Template

1. **Start the Streamlit app**: `streamlit run app.py`
2. **Select your theme** from the dropdown.
3. **Click the preview button** (eye icon) to see it rendered with sample data — no API call needed.
4. **Run a full optimization** to verify it works end-to-end with real AI output and PDF export.
