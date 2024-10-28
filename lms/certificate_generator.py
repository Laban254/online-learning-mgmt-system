from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.utils import timezone
import os

def generate_certificate(user_name, course_title, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, "Certificate of Completion")
    c.drawString(100, height - 150, f"This is to certify that {user_name} has completed the course:")
    c.drawString(100, height - 200, f"{course_title}")
    c.drawString(100, height - 250, f"Date: {timezone.now().strftime('%Y-%m-%d')}")

    c.save()
