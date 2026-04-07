from smtplib import SMTP_SSL
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core.settings import settings
from app.utils.generate_email_htmal_format import generate_email_content
from fastapi import HTTPException, status


def send_email(to, first_message, second_message, subject, action_url, action_text, business_name=settings.name):
    msg = MIMEMultipart('alternative')

    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = f"{business_name} <{settings.smtp_user}>"

    message = f"{first_message}\n\n{second_message}"

    html = generate_email_content(
        business_name=business_name, message_content=first_message, second_message_content=second_message, action_url=action_url, action_text=action_text)

    text_part = MIMEText(message, 'plain')
    html_part = MIMEText(html, 'html')

    msg.attach(text_part)
    msg.attach(html_part)

    context = ssl.create_default_context()

    with SMTP_SSL(host=settings.smtp_server, port=settings.smtp_port, context=context) as server:
        print(
            f"Attempting login for: {settings.smtp_user} on {settings.smtp_server}")
        server.login(user=settings.smtp_user, password=settings.smtp_pass)
        server.send_message(msg=msg)


def send_email_for_ticket_puchase_confirmation(to, action_url, action_text, first_name="Cher", last_name="Participant"):
    subject = f"Confirmation d'achat de billet pour {settings.name}"
    first_message = f"Merci pour votre achat de billet pour PyCon Togo! {first_name},"
    second_message = f"Nous sommes ravis de vous compter parmi les participants à PyCon Togo."

    try:
        send_email(to=to, first_message=first_message, second_message=second_message,
                   subject=subject, action_url=action_url, action_text=action_text)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Failed to send email: {str(e)}")
