import os
from email.message import EmailMessage
from email.utils import formataddr
import smtplib
from dotenv import load_dotenv

from app.database.datas import get_something_by_field
from app.emails_utils.email_templates import (
    attendees,
    render_email_attendees,
    render_sponsor_email,
    render_speaker_email,
)

load_dotenv()


SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.environ.get("SENDER_EMAIL_PASSWORD")
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_SERVER_PORT = os.environ.get("SMTP_SERVER_PORT")
accepted_speakers_list = get_something_by_field("proposals", "accepted", True)


def send_email(subject, body, email_to):
    msg = EmailMessage()

    msg['Subject'] = subject
    msg['From'] = formataddr(('PyCon Togo Organizing Team', SENDER_EMAIL))
    msg['To'] = email_to

    full_message = body
    msg.add_alternative(full_message, subtype='html')

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_SERVER_PORT) as server:
        server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
        server.send_message(msg)


def send_sponsor_email(first_name="Pythonista", email_to="sponsor@example.com"):
    message, subject = render_sponsor_email(first_name=first_name)

    send_email(subject, message, email_to)


def send_attendee_email(email_to=""):
    # message, subject = render_email_attendees()
    message, subject = attendees()

    send_email(subject, message, email_to)


if __name__ == "__main__":
    send_attendee_email(email_to="pycontogo2025attendees@pytogo.org")

    i = 1
    '''for speaker in accepted_speakers_list:
        print(f"Sending email to {speaker['first_name']} at {speaker['email']} ({i}/{len(accepted_speakers_list)})")
        body, subject = render_speaker_email(first_name=speaker['first_name'])
        send_email(subject, body, speaker['email'])
        i += 1
    '''
