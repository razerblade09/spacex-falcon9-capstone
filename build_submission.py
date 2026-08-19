"""
Assemble the single PDF that gets uploaded for the capstone assignment.

The grader reads one file and looks for a completed *presentation*, so the deck
goes first and the written report follows it. A generated cover page states the
GitHub URL and maps every rubric section to a page number, so none of it has to
be inferred from reading order.

Run after build_pptx.js and build_docx.js have been rebuilt and exported to PDF:

    python build_submission.py

Output: "Data Science Capstone Project Report.pdf"
"""
import io
import os

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import Paragraph

ROOT = os.path.dirname(os.path.abspath(__file__))

SLIDES_PDF = os.path.join(ROOT, 'Data_Science_Capstone_Presentation.pdf')
REPORT_PDF = os.path.join(ROOT, 'Data_Science_Capstone_Project_Report.pdf')
OUTPUT_PDF = os.path.join(ROOT, 'Data Science Capstone Project Report.pdf')

GITHUB_URL = 'https://github.com/razerblade09/spacex-falcon9-capstone'
AUTHOR = 'Aaron Vargas'
TITLE = 'Data Science Capstone Project Report'
SUBTITLE = 'SpaceX Falcon 9 First-Stage Landing Prediction'

NAVY = colors.HexColor('#0B1F3A')
BLUE = colors.HexColor('#3B60E4')
GREY = colors.HexColor('#5B6472')

# Rubric section -> 1-based slide number in the deck. Page numbers in the merged
# PDF are derived from these at build time, so the cover can never drift.
SECTIONS = [
    ('Executive Summary', 2),
    ('Introduction', 3),
    ('Data Collection — SpaceX API', 4),
    ('Data Collection — Web Scraping', 5),
    ('Data Wrangling Methodology', 6),
    ('EDA with Data Visualization', 7),
    ('EDA with Data Visualization (results)', 8),
    ('EDA with SQL (queries)', 9),
    ('EDA with SQL (results)', 10),
    ('EDA with SQL (outcome rankings)', 11),
    ('Interactive Visual Analytics — overview', 12),
    ('Folium Map — markers and launch records', 13),
    ('Folium Map — proximity analysis', 14),
    ('Plotly Dash — success rate pie charts', 15),
    ('Plotly Dash — payload vs. launch outcome', 16),
    ('Predictive Analysis — model development', 17),
    ('Predictive Analysis — evaluation and confusion matrix', 18),
    ('Best Model, Conclusion and Insights', 19),
]


def build_cover(n_slides, n_report):
    """Render the cover page and return it as an in-memory PDF."""
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=LETTER)
    width, height = LETTER
    left = 0.9 * inch
    y = height - 1.05 * inch

    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 22)
    c.drawString(left, y, TITLE)
    y -= 0.34 * inch
    c.setFillColor(BLUE)
    c.setFont('Helvetica', 14)
    c.drawString(left, y, SUBTITLE)
    y -= 0.26 * inch
    c.setFillColor(GREY)
    c.setFont('Helvetica', 10.5)
    c.drawString(left, y, f'{AUTHOR}  ·  IBM Applied Data Science Capstone')

    y -= 0.30 * inch
    c.setStrokeColor(BLUE)
    c.setLineWidth(2)
    c.line(left, y, width - left, y)

    # GitHub URL — rubric item 1.1, stated before anything else.
    y -= 0.42 * inch
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 11.5)
    c.drawString(left, y, 'GitHub repository (all completed notebooks and Python files):')
    y -= 0.24 * inch
    c.setFillColor(BLUE)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(left, y, GITHUB_URL)
    c.linkURL(GITHUB_URL, (left, y - 4, left + 4.6 * inch, y + 12), relative=0, thickness=0)

    # What this file contains — rubric item 1.2.
    slides_start, slides_end = 2, 1 + n_slides
    report_start, report_end = slides_end + 1, slides_end + n_report

    y -= 0.46 * inch
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 11.5)
    c.drawString(left, y, 'This single PDF contains both required deliverables:')
    for label, first, last in [
        (f'Completed presentation, all {n_slides} slides', slides_start, slides_end),
        ('Written project report', report_start, report_end),
    ]:
        y -= 0.24 * inch
        c.setFillColor(GREY)
        c.setFont('Helvetica', 11)
        c.drawString(left + 0.2 * inch, y, f'•  {label} — pages {first}–{last}')

    # Section index, so no required section has to be hunted for.
    y -= 0.46 * inch
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 11.5)
    c.drawString(left, y, 'Required sections, by page')
    y -= 0.10 * inch
    c.setStrokeColor(colors.HexColor('#E2E8F5'))
    c.setLineWidth(1)
    c.line(left, y, width - left, y)

    y -= 0.22 * inch
    for name, slide_no in SECTIONS:
        c.setFillColor(GREY)
        c.setFont('Helvetica', 10.5)
        c.drawString(left + 0.2 * inch, y, name)
        c.setFillColor(NAVY)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawRightString(width - left, y, f'page {slide_no + 1}')
        y -= 0.215 * inch

    y -= 0.12 * inch
    c.setFillColor(GREY)
    c.setFont('Helvetica-Oblique', 10)
    note = ('The written report on pages '
            f'{report_start}–{report_end} repeats every section above in long form, '
            'with the same figures and the GitHub link for each stage.')
    style = ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=10,
                           leading=13, textColor=GREY)
    para = Paragraph(note, style)
    w, h = para.wrap(width - 2 * left, 1 * inch)
    para.drawOn(c, left, y - h)

    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf)


def main():
    slides = PdfReader(SLIDES_PDF)
    report = PdfReader(REPORT_PDF)
    cover = build_cover(len(slides.pages), len(report.pages))

    writer = PdfWriter()
    for page in cover.pages:
        writer.add_page(page)
    slides_start = len(writer.pages)
    for page in slides.pages:
        writer.add_page(page)
    report_start = len(writer.pages)
    for page in report.pages:
        writer.add_page(page)

    writer.add_outline_item('Cover and contents', 0)
    deck_root = writer.add_outline_item('Presentation slides', slides_start)
    for name, slide_no in SECTIONS:
        writer.add_outline_item(name, slides_start + slide_no - 1, parent=deck_root)
    writer.add_outline_item('Written project report', report_start)

    writer.add_metadata({
        '/Title': TITLE,
        '/Author': AUTHOR,
        '/Subject': f'{SUBTITLE} — IBM Applied Data Science Capstone',
    })

    with open(OUTPUT_PDF, 'wb') as fh:
        writer.write(fh)

    print(f'Wrote {os.path.basename(OUTPUT_PDF)}')
    print(f'  cover   : page 1')
    print(f'  slides  : pages {slides_start + 1}-{report_start} ({len(slides.pages)} slides)')
    print(f'  report  : pages {report_start + 1}-{len(writer.pages)} ({len(report.pages)} pages)')
    print(f'  total   : {len(writer.pages)} pages, '
          f'{os.path.getsize(OUTPUT_PDF) / 1e6:.2f} MB')


if __name__ == '__main__':
    main()
