from email import encoders
from email.mime.base import MIMEBase
from email.utils import formataddr
import os
from dotenv import load_dotenv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.emails_utils.email_templates import render_email_template

load_dotenv()

sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = "wachioubouraima56@gmail.com"
password = os.environ.get("SENDER_EMAIL_PASSWORD")
smtp_server = os.environ.get("SMTP_SERVER")
smtp_server_port = os.environ.get("SMTP_SERVER_PORT")


def send_email_with_or_without_attachment(body, subject, sender_email=sender_email, receiver_email=receiver_email, password=password, smtp_server=smtp_server, smtp_server_port=smtp_server_port, filename=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = formataddr(('PyCon Togo Team', sender_email))
    msg['To'] = receiver_email

    msg.attach(MIMEText(body, 'html'))

    # Attachment
    if filename:
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f'attachment; filename={os.path.basename(filename)}')
            msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_server_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    first_name = "Pythonistas"

    msgs = [{
        "subject": "[Français] Bienvenu(e) au Challenge 30 Jours de Python",
        "body": f"""\
         <h2>Bonjour {first_name},</h2>
        <p>
        Félicitations ! Tu viens de t’inscrire au <strong>Challenge 30 Jours Python</strong> organisé par <strong>Python Togo</strong> en prélude à <strong>PyCon Togo 2025</strong>, prévu pour le 23 août.
        </p>
        <p>
        <strong>Durée du challenge :</strong> du 23 juillet au 22 août à 23h59. <br>
        Chaque jour, tu recevras un email contenant :
        </p>
        <ul>
        <li>Le défi Python du jour</li>
        <li>Des ressources pour t’aider à le résoudre</li>
        <li>Un lien pour soumettre ta solution</li>
        </ul>
        <p>
        <strong>Soumission :</strong> rends-toi sur notre plateforme 
        <a href="https://challenge.pytogo.org/">https://challenge.pytogo.org/</a> et soumets :
        </p>
        <ul>
        <li>Le lien vers ton code (GitHub, Replit, etc.)</li>
        <li>Une brève explication de ta solution (optionnelle)</li>
        </ul>
        <p>
        <strong>Rejoins notre serveur Discord :</strong> 
        <a href="https://pytogo.org/discord">https://pytogo.org/discord</a><br>
        Une fois à l’intérieur :
        </p>
        <ul>
        <li>Présente-toi dans le canal <code>#challenge-30jours</code></li>
        <li>Signale que tu participes pour recevoir un rôle spécial</li>
        <li>Reste actif pour profiter de l'entraide de la communauté</li>
        </ul>
        <p>
        Tu as un serveur Discord ? N'hésite pas à nous le dire si tu veux collaborer avec nous.
        </p>
        <p>
        Pour toute question ou assistance, écris-nous à <a href="mailto:support@pycon.tg">support@pycon.tg</a>.
        </p>

        """},

        {
        "subject": "[English Version] Welcome to the 30-Day Python Challenge",
        "body": f"""\
        <h2>Hi  {first_name},</h2>
        <p>
        Congratulations! You have successfully registered for the <strong>30-Day Python Challenge</strong> organized by <strong>Python Togo</strong>, in preparation for <strong>PyCon Togo 2025</strong>, taking place on August 23.
        </p>
        <p>
        <strong>Challenge duration:</strong> from July 23 to August 22 at 11:59 PM UTC.<br>
        Each day, you will receive an email containing:
        </p>
        <ul>
        <li>The daily Python challenge</li>
        <li>Helpful learning resources</li>
        <li>A link to submit your solution</li>
        </ul>
        <p>
        <strong>Submission:</strong> go to 
        <a href="https://challenge.pytogo.org/">https://challenge.pytogo.org/</a> and submit:
        </p>
        <ul>
        <li>The link to your code (GitHub, Replit, etc.)</li>
        <li>A brief explanation of your solution (optional)</li>
        </ul>
        <p>
        <strong>Join our Discord server:</strong> 
        <a href="https://pytogo.org/discord">https://pytogo.org/discord</a><br>
        Once inside:
        </p>
        <ul>
        <li>Introduce yourself in the <code>#challenge-30days</code> channel</li>
        <li>Let us know you're participating so we can assign you a special role</li>
        <li>Stay active and engage with the community</li>
        </ul>
        <p>
        Do you already have a Discord server? Let us know if you'd like to collaborate.
        </p>
        <p>
        For help or support, reach out at <a href="mailto:support@pycon.tg">support@pycon.tg</a>.
        </p>
        """
    }
    ]
    for msg in msgs:
        # Render the email body using the template
        body = render_email_template(
            first_name="Omo Wass",
            first_paragraph="We’re happy to inform you that your talk titled <span class='highlight'>Brett Cannon on Python, humans... and packaging</span> has been accepted for PyCon Togo 2025. Congratulations, and thank you for your support!",
            message=msg['body']
        )
        subject = "Test Email"
        filename = "requirements.txt"  # Change this to your file path if needed
        send_email_with_or_without_attachment(body, msg['subject'])
