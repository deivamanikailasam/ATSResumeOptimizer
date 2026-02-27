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
from .sidebar_pro import TEMPLATE as sidebar_pro
from .gradient_wave import TEMPLATE as gradient_wave
from .art_deco import TEMPLATE as art_deco
from .tokyo_metro import TEMPLATE as tokyo_metro
from .neon_glass import TEMPLATE as neon_glass
from .ivory_press import TEMPLATE as ivory_press
from .blueprint import TEMPLATE as blueprint
from .aurora_borealis import TEMPLATE as aurora_borealis
from .terracotta import TEMPLATE as terracotta
from .brushstroke import TEMPLATE as brushstroke
from .obsidian_gold import TEMPLATE as obsidian_gold
from .marble_hall import TEMPLATE as marble_hall
from .vintage_typewriter import TEMPLATE as vintage_typewriter
from .emerald_dusk import TEMPLATE as emerald_dusk
from .lavender_haze import TEMPLATE as lavender_haze
from .copper_forge import TEMPLATE as copper_forge
from .paper_cut import TEMPLATE as paper_cut
from .ink_wash import TEMPLATE as ink_wash
from .sahara_dune import TEMPLATE as sahara_dune
from .glacier_blue import TEMPLATE as glacier_blue
from .crimson_tide import TEMPLATE as crimson_tide
from .bamboo_zen import TEMPLATE as bamboo_zen
from .polaris_star import TEMPLATE as polaris_star
from .rosewood import TEMPLATE as rosewood
from .gazette import TEMPLATE as gazette
from .slate_mosaic import TEMPLATE as slate_mosaic
from .vintage_wine import TEMPLATE as vintage_wine
from .origami import TEMPLATE as origami
from .carbon_fiber import TEMPLATE as carbon_fiber
from .sunset_boulevard import TEMPLATE as sunset_boulevard


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
    ("sidebar_pro", sidebar_pro),
    ("gradient_wave", gradient_wave),
    ("art_deco", art_deco),
    ("tokyo_metro", tokyo_metro),
    ("neon_glass", neon_glass),
    ("ivory_press", ivory_press),
    ("blueprint", blueprint),
    ("aurora_borealis", aurora_borealis),
    ("terracotta", terracotta),
    ("brushstroke", brushstroke),
    ("obsidian_gold", obsidian_gold),
    ("marble_hall", marble_hall),
    ("vintage_typewriter", vintage_typewriter),
    ("emerald_dusk", emerald_dusk),
    ("lavender_haze", lavender_haze),
    ("copper_forge", copper_forge),
    ("paper_cut", paper_cut),
    ("ink_wash", ink_wash),
    ("sahara_dune", sahara_dune),
    ("glacier_blue", glacier_blue),
    ("crimson_tide", crimson_tide),
    ("bamboo_zen", bamboo_zen),
    ("polaris_star", polaris_star),
    ("rosewood", rosewood),
    ("gazette", gazette),
    ("slate_mosaic", slate_mosaic),
    ("vintage_wine", vintage_wine),
    ("origami", origami),
    ("carbon_fiber", carbon_fiber),
    ("sunset_boulevard", sunset_boulevard),
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
