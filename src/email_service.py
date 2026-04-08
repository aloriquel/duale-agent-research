import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, RECIPIENT_EMAIL

class EmailService:
    def send_email(self, subject, html_content):
        """Send the report via email."""
        msg = MIMEMultipart('related')
        msg['From'] = SMTP_USERNAME
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject

        # Brand CSS and Wrapper
        template = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #FAFAFA; color: #242424; margin: 0; padding: 20px; }}
                .container {{ max-width: 800px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 8px; border-top: 5px solid #053264; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                h1, h2, h3 {{ color: #053264; }}
                a {{ color: #AF68D0; text-decoration: none; }}
                .cta-button {{ display: inline-block; background-color: #CCFFBC; color: #053264; padding: 12px 24px; text-decoration: none; font-weight: bold; border-radius: 4px; margin-top: 20px; }}
                .signature {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #eaeaea; }}
            </style>
        </head>
        <body>
            <div class="container">
                {html_content}
                <div style="text-align: center; margin-top: 40px;">
                    <a href="https://www.duale.es" class="cta-button">Visitar duale.es</a>
                </div>
                <div class="signature">
                    <p><b>Duale Research Agent</b></p>
                    <img src="cid:duale_logo" width="150" alt="Duale Logo">
                </div>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(template, 'html'))

        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-ID', '<duale_logo>')
                img.add_header('Content-Disposition', 'inline', filename='logo.png')
                msg.attach(img)

        try:
            print(f"Connecting to {SMTP_SERVER}...")
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, RECIPIENT_EMAIL, msg.as_string())
            server.quit()
            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
