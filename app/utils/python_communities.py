

from smtplib import SMTP_SSL
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.settings import settings
from app.utils.generate_email_htmal_format import generate_email, generate_plain_text_email
from fastapi import HTTPException, status

SENDER_EMAIL = "exemple@pytogo.org"
SENDER_EMAIL_PASSWORD = "your_email_password"
SENDER_NAME = "your_name_or_business_name"


def send_email(to, org_name="Python Community", subject=f"Support Request from {settings.name} team"):
    msg = MIMEMultipart('alternative')

    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg['Cc'] = f"Python Software Community Togo <{settings.smtp_user}>"

    html = generate_email(org_name=org_name)
    message = generate_plain_text_email(org_name=org_name)

    text_part = MIMEText(message, 'plain')
    html_part = MIMEText(html, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    context = ssl.create_default_context()

    with SMTP_SSL(host=settings.smtp_server, port=settings.smtp_port, context=context) as server:
        print(
            f"Attempting login for: {SENDER_EMAIL} on {settings.smtp_server}")
        server.login(user=SENDER_EMAIL, password=SENDER_EMAIL_PASSWORD)
        server.send_message(msg=msg)
