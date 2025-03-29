import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile

def generate_qr_code(ticket_data):
    """Generates a QR code for the ticket data."""
    qr = qrcode.make(ticket_data)
    qr_io = BytesIO()
    qr.save(qr_io, format="PNG")
    qr_io.seek(0)
    return qr_io

def generate_ticket_pdf(ticket_info):
    """Generates a PDF ticket containing the ticket information."""
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Movie Ticket: {ticket_info['movie_name']}")
    p.drawString(100, 730, f"Seat Number: {ticket_info['seat_number']}")
    p.drawString(100, 710, f"Showtime: {ticket_info['showtime']}")
    p.drawString(100, 690, f"User: {ticket_info['user_name']}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def send_ticket_email(user_email, ticket_info):
    """Sends an email with the ticket and QR code attached."""
    subject = "Your Movie Ticket Confirmation"
    body = f"Dear {ticket_info['user_name']},\n\nHere is your movie ticket for {ticket_info['movie_name']}.\nEnjoy your show!\n\nBest,\nMovie Ticket System"
    email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [user_email])

    # Generate QR Code
    qr_data = f"{ticket_info['movie_name']}, {ticket_info['seat_number']}, {ticket_info['showtime']}"
    qr_io = generate_qr_code(qr_data)
    email.attach("ticket_qr.png", qr_io.getvalue(), "image/png")

    # Generate Ticket PDF
    ticket_pdf = generate_ticket_pdf(ticket_info)
    email.attach("ticket.pdf", ticket_pdf.getvalue(), "application/pdf")

    email.send()
