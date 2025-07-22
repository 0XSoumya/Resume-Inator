from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO

def create_resume_pdf(resume_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Heading', fontSize=14, leading=18, spaceAfter=6, spaceBefore=12, textColor=colors.HexColor("#2e4053")))
    styles.add(ParagraphStyle(name='Body', fontSize=11, leading=14))
    styles.add(ParagraphStyle(name='SectionTitle', fontSize=12, leading=14, spaceAfter=4, spaceBefore=8, textColor=colors.black, fontName='Helvetica-Bold'))

    content = []

    # --- Header ---
    full_name = resume_data.get("name", "Your Name")
    contact = " | ".join(filter(None, [resume_data.get("email"), resume_data.get("phone"), resume_data.get("linkedin")]))

    content.append(Paragraph(f"<b>{full_name}</b>", styles["Title"]))
    content.append(Paragraph(contact, styles["Normal"]))
    content.append(Spacer(1, 8))
    content.append(HRFlowable(width="100%", color=colors.grey, thickness=1))
    content.append(Spacer(1, 12))

    # --- Section builder with lines ---
    def add_section(title, text):
        if text:
            content.append(Spacer(1, 6))
            content.append(Paragraph(title, styles["SectionTitle"]))
            content.append(HRFlowable(width="100%", color=colors.HexColor("#cccccc"), thickness=0.5))
            content.append(Spacer(1, 6))
            for line in text.strip().split('\n'):
                if line.strip():
                    content.append(Paragraph(line.strip(), styles["Body"]))
            content.append(Spacer(1, 10))

    # --- Add Sections ---
    add_section("Summary", resume_data.get("summary"))
    add_section("Experience", resume_data.get("experience"))
    add_section("Education", resume_data.get("education"))
    add_section("Skills", resume_data.get("skills"))

    # --- Build PDF ---
    doc.build(content)
    return buffer.getvalue()
