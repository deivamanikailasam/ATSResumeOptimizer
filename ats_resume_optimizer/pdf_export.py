"""Convert Markdown resume to PDF (using xhtml2pdf for Windows compatibility)."""

from pathlib import Path

from markdown import markdown as md_to_html
from xhtml2pdf import pisa


def markdown_to_pdf(markdown_text: str, output_path: Path) -> None:
    """Render Markdown to HTML and write a PDF to output_path."""
    html = md_to_html(markdown_text, output_format="html5")
    html_doc = f"""
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          body {{
            font-family: Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.3;
          }}
          h1, h2, h3 {{
            margin-bottom: 0.2em;
          }}
          ul {{
            margin-top: 0.1em;
          }}
        </style>
      </head>
      <body>
        {html}
      </body>
    </html>
    """
    with open(output_path, "w+b") as dest_file:
        status = pisa.CreatePDF(html_doc, dest=dest_file, encoding="utf-8")
    if status.err:
        raise RuntimeError("PDF generation failed (xhtml2pdf reported errors).")
