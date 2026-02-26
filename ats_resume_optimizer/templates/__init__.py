from collections import OrderedDict

from ._colors import hex_to_rgb, rgb_to_hex, lighten, darken  # noqa: F401

from .modern_minimal import TEMPLATE as modern_minimal
from .executive_classic import TEMPLATE as executive_classic
from .creative_bold import TEMPLATE as creative_bold
from .tech_professional import TEMPLATE as tech_professional
from .elegant_serif import TEMPLATE as elegant_serif
from .nordic_frost import TEMPLATE as nordic_frost
from .midnight_luxe import TEMPLATE as midnight_luxe
from .swiss_grid import TEMPLATE as swiss_grid
from .coral_ribbon import TEMPLATE as coral_ribbon
from .monograph import TEMPLATE as monograph


TEMPLATES = OrderedDict([
    ("modern_minimal", modern_minimal),
    ("executive_classic", executive_classic),
    ("creative_bold", creative_bold),
    ("tech_professional", tech_professional),
    ("elegant_serif", elegant_serif),
    ("nordic_frost", nordic_frost),
    ("midnight_luxe", midnight_luxe),
    ("swiss_grid", swiss_grid),
    ("coral_ribbon", coral_ribbon),
    ("monograph", monograph),
])


def get_template(template_id: str) -> dict:
    return TEMPLATES[template_id]


def get_template_choices() -> list[tuple[str, str]]:
    return [(tid, t["name"]) for tid, t in TEMPLATES.items()]


def render_resume(template_id: str, content_html: str, primary_color: str) -> str:
    return TEMPLATES[template_id]["render"](content_html, primary_color)


# ---------------------------------------------------------------------------
# Shared HTML structure guide – sent to the LLM so it knows what markup to
# produce.  Every template's CSS targets these same semantic class names.
# ---------------------------------------------------------------------------

CONTENT_STRUCTURE = """\
Generate the resume as HTML using **exactly** this structure.
Do NOT include <html>, <head>, <body>, or <style> tags – only the inner content.
Use the class names shown below so the selected theme CSS can style them.

<div class="resume-header">
    <h1>FULL NAME</h1>
    <div class="contact-info">
        <span>email@example.com</span>
        <span>(123) 456-7890</span>
        <span>City, State</span>
        <span>linkedin.com/in/username</span>
    </div>
</div>

<div class="resume-section summary">
    <h2>Professional Summary</h2>
    <p>2-3 sentence summary of qualifications and value proposition.</p>
</div>

<div class="resume-section skills">
    <h2>Technical Skills</h2>
    <div class="skills-grid">
        <div class="skill-category">
            <strong>Category:</strong>
            <span class="skill-tag">Skill 1</span>
            <span class="skill-tag">Skill 2</span>
        </div>
        <!-- more categories -->
    </div>
</div>

<div class="resume-section experience">
    <h2>Professional Experience</h2>
    <div class="experience-item">
        <div class="item-header">
            <h3>Job Title</h3>
            <span class="date">Month Year – Present</span>
        </div>
        <div class="company">Company Name · City, State</div>
        <ul>
            <li>Action verb + accomplishment with quantifiable impact.</li>
        </ul>
    </div>
    <!-- more experience items -->
</div>

<div class="resume-section education">
    <h2>Education</h2>
    <div class="education-item">
        <div class="item-header">
            <h3>Degree Name</h3>
            <span class="date">Year – Year</span>
        </div>
        <div class="company">University Name · City, State</div>
    </div>
</div>

<div class="resume-section projects">
    <h2>Notable Projects</h2>
    <div class="project-item">
        <div class="item-header">
            <h3>Project Name</h3>
            <span class="date">Year</span>
        </div>
        <p>Brief description with technologies and impact.</p>
    </div>
</div>

<div class="resume-section certifications">
    <h2>Certifications</h2>
    <ul class="cert-list">
        <li><strong>Certification Name</strong> – Issuing Org (Year)</li>
    </ul>
</div>
"""
