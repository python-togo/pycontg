def render_email_template( message=""):
    """
    Renders the email template with the provided body and subject.
    
    Args:
        body (str): The body of the email.
        subject (str): The subject of the email.
    
    Returns:
        str: The rendered HTML email template.
    """
    html = f"""\
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
    body {{
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    color: #333333;
    background-color: #ffffff;
    }}
    .container {{
    max-width: 600px;
    margin: auto;
    padding: 20px;
    }}
    .logo {{
    text-align: center;
    margin-bottom: 20px;
    }}
    .logo img {{
    width: 150px;
    }}
    .content h2 {{
    color: #111111;
    }}
    .content p {{
    line-height: 1.6;
    }}
    .highlight {{
    font-weight: bold;
    }}
    a {{
    color: #007bff;
    text-decoration: none;
    }}
    .footer {{
    text-align: center;
    font-size: 14px;
    margin-top: 30px;
    color: #666;
    }}
    .social-icons {{
    margin-top: 10px;
    }}
    .social-icons img {{
    width: 24px;
    margin: 0 5px;
    vertical-align: middle;
    }}
    .sponsors {{
    margin-top: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    flex-wrap: wrap;
    }}
    .sponsors img {{
    height: 50px;
    object-fit: contain;
    }}
    @media (max-width: 600px) {{
    .container {{
        padding: 15px;
    }}
    .content {{
        padding: 15px;
    }}
    }}
</style>
</head>
<body>
<div class="container">
    <div class="logo">
    <img src="https://pycontg.pytogo.org/static/images/pycontogo.png" alt="PyCon TOGO 2025 Logo">
    </div>
    <div class="content">

       {message}

        <p><strong>Best regards,</strong></p>
    </div>

    <div class="footer">
        

        <!-- Sponsors -->
        <div class="sponsors">
            <a href="https://www.python.org/psf-landing/" target="_blank"><img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1744077536/psf-logo_xk6r0e.png" alt="psf"></a>
            <a href="https://www.afpy.org/" target="_blank"><img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1757104352/afpy_mizqfd.png" alt="afpy"></a>
            <a href="https://blackpythondevs.com/" target="_blank"><img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1751558100/bpd_stacked_us5ika.png" alt="bpd"></a>
            <a href="https://tahaga.com" target="_blank"><img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1753966042/Logo_TAHAGA_02_Plan_de_travail_1_5_rh5s9g.jpg" alt="tahaga"></a>
            <a href="https://wearedigijob.com/" target="_blank"><img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1755176153/digijoblogo_tkbhns.png" alt="digijob"></a>
            <a href="https://www.djangoproject.com/foundation/" target="_blank"><img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1757104362/django-logo-positive_ziry9u.png" alt="django"></a>
        </div>
        <br><br>
        <p><strong>Python Togo Community</strong><br>
        <a href="https://www.pytogo.org/">Python TOGO</a><br>
        Bd de la KARA, +22898273805 / +22898776682 / +22892555987, LOME</p>

        <div class="social-icons">
            <a href="https://www.linkedin.com/company/python-togo/"><img src="https://cdn-icons-png.flaticon.com/512/145/145807.png" alt="LinkedIn"></a>
            <a href="https://pytogo.org/discord"><img src="https://cdn-icons-png.flaticon.com/512/5968/5968756.png" alt="Discord"></a>
            <a href="https://github.com/pytogo-org"><img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="GitHub"></a>
            <a href="https://x.com/pytogo_org"><img src="https://cdn-icons-png.flaticon.com/512/733/733635.png" alt="X/Twitter"></a>
            <a href="https://www.youtube.com/@PythonTogo"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" alt="YouTube"></a>
            <a href="#"><img src="https://cdn-icons-png.flaticon.com/512/1384/1384063.png" alt="Instagram"></a>
        </div>
    </div>
</div>
</body>
</html>
"""

    return html



def render_sponsor_email(first_name="Pythonista"):
    html = f"""\
    <div style="font-family: Arial, sans-serif; color: #333333; line-height: 1.6; padding: 20px;">

  <!-- English Section -->
  <h2 style="color: #1a73e8;">🤝 Thank You for Your Interest in Sponsoring PyCon Togo 2025</h2>
    
  <p>Dear <strong>{first_name}</strong>,</p>

  <p>We sincerely appreciate your interest in sponsoring <strong>PyCon Togo 2025</strong>. Your support helps us strengthen the Python and tech ecosystem in Togo.</p>

  <p>Our team has received your submission. One of our members will reach out to you shortly to discuss possible collaboration opportunities and finalize sponsorship arrangements.</p>

  <p>In the meantime, feel free to send us:</p>
  <ul style="padding-left: 20px;">
    <li>Your preferred sponsorship level or package</li>
    <li>Your brand/logo guidelines (if available)</li>
    <li>Any questions or expectations you may have</li>
  </ul>

  <p>We’re looking forward to partnering with you!</p>

  <p>Best regards,<br>
  The PyCon Togo 2025 Team<br>


  <hr style="margin: 40px 0; border: none; border-top: 1px solid #cccccc;">

  <!-- French Section -->
  <h2 style="color: #1a73e8;">🤝 Merci pour votre intérêt à sponsoriser PyCon Togo 2025</h2>

  <p>Cher·e <strong>{first_name}</strong>,</p>

  <p>Nous vous remercions sincèrement pour votre intérêt à sponsoriser <strong>PyCon Togo 2025</strong>. Votre soutien contribue au développement de l'écosystème Python et technologique au Togo.</p>

  <p>Nous avons bien reçu votre soumission. Un membre de notre équipe vous contactera sous peu pour discuter des opportunités de collaboration et finaliser les modalités de sponsoring.</p>

  <p>En attendant, vous pouvez déjà nous envoyer :</p>
  <ul style="padding-left: 20px;">
    <li>Le niveau ou le type de sponsoring souhaité</li>
    <li>Votre charte graphique ou logo (si disponible)</li>
    <li>Toute question ou attente spécifique que vous pourriez avoir</li>
  </ul>

  <p>Nous sommes impatients de collaborer avec vous !</p>

  <p>Cordialement,<br>
  L’équipe PyCon Togo 2025<br>


</div>
    """
    body = render_email_template(message=html)
    subject = "🤝 Thank You for Your Interest in Sponsoring PyCon Togo 2025"
    return body, subject

def render_email_attendees():
    html = f"""\
    <div style="font-family: Arial, sans-serif; color: #333333;; line-height: 1.6; padding: 20px;">

  <!-- Version française -->
  <p>Bonjour Participant·e,</p>

  <p>
    Nous vous remercions chaleureusement pour avoir rejoint la toute première <strong>PyCon Togo</strong> ! 
    Que ce soit <strong>en personne</strong> ou <strong>en ligne via notre live YouTube</strong>, 
    votre présence et vos échanges ont rendu cet événement spécial et enrichissant pour toute l’Afrique 
    (Nigeria, Togo, Bénin, Côte d’Ivoire, Ghana…).
  </p>

  <p>Pour continuer à nous améliorer et rester en contact, voici quelques ressources utiles :</p>
  <ul>
    <li><a href="https://pycontg.pytogo.org/feedback" style="color: #006400; text-decoration: underline;">Donnez votre feedback</a></li>
    <li><a href="https://www.youtube.com/live/sOAoUH0pZNU?si=Fk1i7dsn4HnQcbWb" style="color: #006400; text-decoration: underline;">Regardez l’événement à la demande</a></li>
    <li><a href="https://pycontg.pytogo.org/talents" style="color: #006400; text-decoration: underline;">Opportunités avec notre partenaire DigiJob</a></li>
  </ul>

  <p>
    Merci encore pour votre enthousiasme et votre soutien. Nous espérons vous retrouver lors de nos prochains événements !
  </p>

  <p>Cordialement,<br><strong>L’équipe PyCon Togo</strong></p>

  <hr style="border: 0; border-top: 1px solid #006400; margin: 20px 0;">

  <!-- English Version -->
  <p>Hello Participant,</p>

  <p>
    We sincerely thank you for joining the very first <strong>PyCon Togo</strong>! 
    Whether you participated <strong>in person</strong> or <strong>online via our YouTube live</strong>, 
    your presence and contributions made this event special and engaging across Africa 
    (Nigeria, Togo, Benin, Ivory Coast, Ghana…).
  </p>

  <p>To help us improve and stay connected, here are some useful resources:</p>
  <ul>
    <li><a href="https://pycontg.pytogo.org/feedback" style="color: #006400; text-decoration: underline;">Give your feedback</a></li>
    <li><a href="https://www.youtube.com/live/sOAoUH0pZNU?si=Fk1i7dsn4HnQcbWb" style="color: #006400; text-decoration: underline;">Watch the event on demand</a></li>
    <li><a href="https://pycontg.pytogo.org/talents" style="color: #006400; text-decoration: underline;">Opportunities with our partner DigiJob</a></li>
  </ul>

  <p>
    Thank you again for your enthusiasm and support. We hope to see you at our future events!
  </p>

  <p>Best regards,<br><strong>PyCon Togo Team</strong></p>

</div>
"""
    body = render_email_template(message=html)
    subject = "Merci pour votre participation à PyCon Togo 2025 / Thank you for joining PyCon Togo 2025"
    return body, 

def render_speaker_email(first_name="Speakers"):
  subject = "Thank You, Photos & Feedback – PyCon Togo 2025"
  html = f"""
   <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
    <p>Dear {first_name},</p>

    <p>
    On behalf of the entire <strong>PyCon Togo 2025</strong> organizing team, we would like to sincerely thank you 
    for your talk and for contributing to the success of this first-ever Python conference in Togo. 
    Your presence and insights greatly enriched the experience for all participants.
    </p>

    <p>
    We also want to apologize for the delay in delivering the event photos. 
    We took some extra time to sort and organize them so we could share the best memories with you.
    </p>

    <p>
    👉 You can access the PyCon Togo 2025 photos through this link: 
    <a href="https://drive.google.com/drive/folders/1-OrYoTasN_DnC_v6A4JFYtu4utgo2OIe?usp=sharing" style="color: #1a73e8;">View Photos</a>
    </p>


   <p>
    We would also love to hear your thoughts about the event. 
    Your feedback is very important to us and will help us improve future editions.  
    Please take a few minutes to fill out the feedback form here:  
    <a href="https://pycontg.pytogo.org/feedback" style="color: #1a73e8;">Give Feedback</a>
   </p>

    <p>
    We hope these pictures bring back great memories, and please feel free to keep or share them.
    </p>

    <p>
    Once again, thank you for your valuable contribution to PyCon Togo. 
    We look forward to staying in touch and hopefully seeing you again at future editions.
    </p>


    <em>PyCon Togo Organizing Team</em></p>
  </div>

  """
  body = render_email_template(message=html)
  return body, subject


def attendees():
  subject = "[URGENT] Tes photos et ton feedback - PyCon Togo 2025 | Your Photos & Feedback - PyCon Togo 2025"

  body = """
  <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333; line-height: 1.6;">

  <!-- FRANÇAIS -->
  <p><strong>Salut Pythonista,</strong></p>

  <p>Merci encore pour ta participation à <strong>PyCon Togo 2025</strong>. Ta présence a vraiment contribué au succès de l’événement.</p>

  <p>On s’excuse pour le retard dans la mise à disposition des photos. Elles sont maintenant disponibles&nbsp;:
    <a href="https://drive.google.com/drive/folders/1Xk8lejAQXBIPjPf1UHnuUmZJ5sEYNPM1?usp=sharing" target="_blank">Voir / télécharger les photos</a>.
  </p>

  <p>On aimerait beaucoup avoir ton retour pour améliorer les prochaines éditions. Dis-nous ce que tu as aimé, ce que tu as moins aimé, et tes idées pour rendre PyCon Togo encore meilleur&nbsp;:
    <a href="https://pycontg.pytogo.org/feedback" target="_blank">Ton avis nous intéresse, Donne ton avis ici</a>.
  </p>

  <p>Si tu veux partager ton expérience dans un post ou un article de blog, tu peux utiliser <strong>Medium</strong> ou <strong>Hashnode</strong>.
     Partage ensuite le lien sur notre serveur Discord dans le channel <strong>#social-posts</strong>
     (<a href="https://pytogo.org/discord" target="_blank">rejoindre le serveur</a>),
     ou tague-nous sur les réseaux sociaux avec les hashtags officiels
     <strong>#PyConTogo2025</strong> et <strong>#PyConTogo</strong>. On sera ravis de lire, commenter et relayer tes contenus.
  </p>

  <p>Merci encore pour ton engagement. D’autres activités et surprises arrivent bientôt, et tes idées et ton implication comptent vraiment pour la suite.</p>

  <p>L’équipe <strong>PyCon Togo</strong></p>

  <hr style="margin: 28px 0; border: none; border-top: 1px solid #ddd;">

  <!-- ENGLISH -->
  <p><strong>Hi Pythonista,</strong></p>

  <p>Thank you again for your participation in <strong>PyCon Togo 2025</strong>. Your presence really helped make the event a success.</p>

  <p>We apologize for the delay in delivering the photos. They are now available:
    <a href="https://drive.google.com/drive/folders/1Xk8lejAQXBIPjPf1UHnuUmZJ5sEYNPM1?usp=sharing" target="_blank">View / download the photos</a>.
  </p>

  <p>We’d love to get your feedback to improve future editions. Tell us what you liked, what you didn’t like, and your ideas for making PyCon Togo even better:
    <a href="https://pycontg.pytogo.org/feedback" target="_blank">Give Feedback</a>.
  </p>

  <p>If you want to share your experience in a post or blog, you can use <strong>Medium</strong> or <strong>Hashnode</strong>.
     Then share the link on our Discord server in the <strong>#social-posts</strong> channel
     (<a href="https://pytogo.org/discord" target="_blank">join the server</a>),
     or tag us on social media using the official hashtags
     <strong>#PyConTogo2025</strong> and <strong>#PyConTogo</strong>. We’ll be happy to read, comment, and amplify your posts.
  </p>

  <p>Thanks again for your engagement. More activities and surprises are coming soon, and your ideas and involvement really matter for the next editions.</p>

  <p>The <strong>PyCon Togo</strong> Team</p>

</div>
"""
  body = render_email_template(message=body)
  return body, subject



if __name__ == "__main__":
    body, subject = attendees()
    print(body)
    #print(subject)

