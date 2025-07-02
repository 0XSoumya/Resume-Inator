# pdf_utils.py
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        # Header is usually not used for resumes, but kept for FPDF structure
        # self.set_font('Arial', 'B', 16)
        # self.cell(0, 10, self.title, 0, 1, 'C')
        # self.ln(10)
        pass

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_line_width(0.5)
        # Draw a line under the title
        self.line(self.get_x(), self.get_y(), self.get_x() + self.w - 2*self.l_margin, self.get_y())
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        # Replace common markdown bullet points with a PDF-friendly character
        body = body.replace('* ', '• ')
        body = body.replace('- ', '• ')
        self.multi_cell(0, 7, body)
        self.ln(10)

def create_resume_pdf(resume_data):
    """
    Creates a PDF of the resume data.
    resume_data is a dictionary with keys like 'name', 'email', 'phone', 'linkedin',
    'summary', 'experience', 'education', 'skills'.
    """
    pdf = PDF()
    pdf.set_auto_page_break(auto_page_break=True, margin=15)
    pdf.add_page()

    # Personal Information
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 10, resume_data.get('name', 'Your Name'), 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    contact_info = []
    if resume_data.get('email'):
        contact_info.append(resume_data['email'])
    if resume_data.get('phone'):
        contact_info.append(resume_data['phone'])
    if resume_data.get('linkedin'):
        contact_info.append(resume_data['linkedin'])
    pdf.cell(0, 7, " | ".join(contact_info), 0, 1, 'C')
    pdf.ln(10)

    # Summary
    if resume_data.get('summary'):
        pdf.chapter_title('Summary')
        pdf.chapter_body(resume_data['summary'])

    # Experience
    if resume_data.get('experience'):
        pdf.chapter_title('Experience')
        pdf.chapter_body(resume_data['experience'])

    # Education
    if resume_data.get('education'):
        pdf.chapter_title('Education')
        pdf.chapter_body(resume_data['education'])

    # Skills
    if resume_data.get('skills'):
        pdf.chapter_title('Skills')
        pdf.chapter_body(resume_data['skills'])

    # Output PDF as bytes
    # 'S' returns as string, then encode to bytes. Latin1 is a safe encoding for PDF.
    return pdf.output(dest='S').encode('latin1')