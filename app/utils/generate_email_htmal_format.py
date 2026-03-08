hmlt_template = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Template</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      background-color: #f4f6f8;
      font-family: Arial, sans-serif;
    }

    .container {
      width: 100%;
      padding: 20px 0;
      display: flex;
      justify-content: center;
    }

    .email-card {
      width: 100%;
      max-width: 600px;
      background: #ffffff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .header {
      padding: 20px;
      text-align: center;
      color: #ffffff;
      font-size: 20px;
      font-weight: bold;
    }

    .content {
      padding: 25px;
      color: #333333;
      line-height: 1.6;
      font-size: 15px;
    }

    .content h1 {
      font-size: 18px;
      margin-bottom: 10px;
    }

    .button-container {
      text-align: center;
      margin: 25px 0;
    }

    .cta-button {
      background-color: #9bc6a6;
      color: #ffffff !important;
      padding: 12px 20px;
      text-decoration: none;
      border-radius: 5px;
      display: inline-block;
      font-weight: bold;
    }

    .cta-button:hover {
      background-color: #84b495;
    }

    .footer {
      background-color: #f0f0f0;
      padding: 20px;
      text-align: center;
      font-size: 13px;
      color: #848e9c;
    }

    .signature {
      margin-top: 30px;
    }

    @media only screen and (max-width: 600px) {
      .content {
        padding: 15px;
      }
    }
  </style>
</head>
<body>

  <div class="container">
    <div class="email-card">

      <!-- HEADER -->
            <div class="header">
                <img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1774223918/5_mvgkea.png" alt="Logo"
                    style="height: 300px; display:block; margin:0 auto 10px; width: 300px;">
            </div>


      <!-- CONTENT -->
      <div class="content">
        <h1>{{TITLE}}</h1>

        <p>Bonjour {{USER_NAME}},</p>

        <p>
          {{MAIN_MESSAGE}}
        </p>

        <!-- CTA BUTTON -->
        {{action_button}}

        <p>
          {{SECONDARY_MESSAGE}}
        </p>

        <!-- SIGNATURE -->
        <div class="signature">
          <p>Cordialement,</p>
          <p><strong>L'équipe {{APP_NAME}}</strong></p>
        </div>
      </div>

      <!-- FOOTER -->
      <div class="footer">
        <p>{{FOOTER_TEXT}}</p>
        <p>
          <a href="{{UNSUBSCRIBE_LINK}}" style="color:#848e9c; text-decoration: underline;">
            Se désinscrire
          </a>
        </p>
      </div>

    </div>
  </div>

</body>
</html>
"""


def generate_email(org_name="Python Community"):
    html_content = f"""
    <!DOCTYPE html>
    <html>

    <body style="margin:0; padding:0; background:#f4f4f4; font-family:Arial, sans-serif;">

        <table width="100%" cellpadding="0" cellspacing="0" style="padding:20px;">
            <tr>
                <td align="center">

                    <table width="600" cellpadding="0" cellspacing="0"
                        style="background:#ffffff; border-radius:8px; padding:25px;">

                        <!-- Logo -->
                        <tr>
                            <td align="center">
                                <img src="https://res.cloudinary.com/dvg7vky5o/image/upload/v1774223918/5_mvgkea.png"
                                    alt="PyCon Togo 2026" width="140"
                                    style="display:block; max-width:100%; height:auto;">
                            </td>
                        </tr>

                        <!-- Body -->
                        <tr>
                            <td style="font-size:14px; color:#555; line-height:1.6; padding-top:15px;">

                                <p>Dear {org_name} Team,</p>

                                <p>
                                    My name is <strong>Wachiou Bouraima (Wasiu Ibrahim)</strong>, and I am a member of the
                                    organizing team of <strong>PyCon Togo 2026</strong>.
                                </p>

                                <p>
                                    Following a successful first edition, we are currently preparing our second edition, with
                                    the ambition of strengthening the Python ecosystem in Togo and across West Africa.
                                </p>

                                <p>
                                    In this context, I am reaching out to connect with Python communities around the world and
                                    learn from teams like yours.
                                </p>

                                <p>
                                    I came across <strong>{org_name}</strong> and was impressed by your work in growing your
                                    local Python community.
                                </p>

                                <p>
                                    Your support could greatly help us as we continue building and scaling our conference.
                                </p>

                                <p>We would especially appreciate:</p>

                                <ul style="padding-left:18px;">
                                    <li>Insights on organizing and scaling a PyCon event</li>
                                    <li>Guidance on sponsorship strategies</li>
                                    <li>Introductions to potential partners or sponsors</li>
                                    <li>Sharing our initiative within your community</li>
                                </ul>

                                <p>
                                    Learn more about our event:<br>
                                    <a href="https://pycon.pytogo.org"
                                      style="color:#3776AB; word-break:break-word;">
                                        https://pycon.pytogo.org
                                    </a>
                                </p>

                                <p>
                                    We would be happy to schedule a short call if you are available.
                                </p>

                                <p>
                                    Thank you for your time and for supporting the global Python community.
                                </p>

                                <p>
                                    Best regards,<br>
                                    <strong>Wachiou Bouraima (Wasiu Ibrahim)</strong><br>
                                    PyCon Togo Organizing Team
                                </p>

                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>

    </html>
    """
    return html_content


def generate_plain_text_email(org_name="Python Community"):
    return f"""
    Dear {org_name} Team,

    My name is Wachiou Bouraima (Wasiu Ibrahim), and I am a member of the organizing team of PyCon Togo 2026.

    Following a successful first edition, we are currently preparing our second edition, with the ambition of strengthening the Python ecosystem in Togo and across West Africa.

    In this context, I am reaching out to connect with Python communities around the world and learn from teams like yours.

    I came across {org_name} and was impressed by your work in growing your local Python community.

    Your support could greatly help us as we continue building and scaling our conference.

    We would especially appreciate:
    - Insights on organizing and scaling a PyCon event
    - Guidance on sponsorship strategies
    - Introductions to potential partners or sponsors
    - Sharing our initiative within your community

    Learn more about our event:
    https://pycon.pytogo.org

    We would be happy to schedule a short call if you are available.

    Thank you for your time and for supporting the global Python community.

    Best regards,
    Wachiou Bouraima (Wasiu Ibrahim)
    PyCon Togo Organizing Team
    """


def generate_action_button(action_url, action_text):
    if action_url and action_text:
        return f"""
        <div class="button-container">
          <a href="{action_url}" class="cta-button">{action_text}</a>
        </div>
        """
    return ""


def generate_email_content(business_name, message_content, second_message_content, action_url=None, action_text=None):
    action_button = generate_action_button(action_url, action_text)
    return hmlt_template.replace("{{APP_NAME}}", business_name) \
        .replace("{{TITLE}}", "Notification de " + business_name) \
        .replace("{{USER_NAME}}", "Utilisateur") \
        .replace("{{MAIN_MESSAGE}}", message_content) \
        .replace("{{SECONDARY_MESSAGE}}", second_message_content) \
        .replace("{{action_button}}", action_button) \
        .replace("{{FOOTER_TEXT}}", f"Vous recevez cet email car vous êtes inscrit sur {business_name}.") \
        .replace("{{UNSUBSCRIBE_LINK}}", "https://www.pycontg.pytogo.org/unsubscribe")


if __name__ == "__main__":
    # Example usage
    hmlt_template = generate_email(
        org_name="Python Community",
        event="votre événement local",
        business_name="PyCon Togo"
    )

    print(hmlt_template)
