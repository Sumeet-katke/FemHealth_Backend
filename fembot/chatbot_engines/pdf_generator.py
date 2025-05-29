from fpdf import FPDF
import os
from datetime import datetime


class PlanPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Your Personalized Wellness Plan", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True, align="L")
        self.ln(5)

    def chapter_body(self, items, icon):
        self.set_font("Arial", "", 12)
        for item in items:
            self.cell(0, 10, f"{icon} {item}", ln=True)
        self.ln(5)
from django.conf import settings
def generate_plan_pdf(user_id,  diet, exercise, mood):
    pdf = PlanPDF()
    pdf.add_page()
    # Add the Unicode font
    font_path = os.path.join(settings.BASE_DIR, "fembot/static/fonts/DejaVuSans.ttf")
    pdf.add_font('DejaVu', '', font_path, uni=True)

    # Set the font
    pdf.set_font('DejaVu', '', 14)

    pdf.chapter_title(f"User ID: {user_id}")
    # pdf.chapter_title(f"Diagnosis: {diagnosis.capitalize()}")
    pdf.chapter_title(f"Mood: {mood.capitalize()}")

    pdf.chapter_title(" Diet Recommendations:")
    pdf.chapter_body(diet, "")

    pdf.chapter_title(" Exercise Suggestions:")
    pdf.chapter_body(exercise, "")

    if not os.path.exists("plans/pdfs"):
        os.makedirs("plans/pdfs")

    filename = f"plans/pdfs/{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
