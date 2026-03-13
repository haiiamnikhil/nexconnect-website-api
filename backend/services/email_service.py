import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_pass = os.getenv("SMTP_PASS", "")
        # Assuming we are running from the backend directory, so 'templates' is available
        try:
            self.env = Environment(loader=FileSystemLoader("templates"))
        except Exception:
            # Fallback if running from another directory
            self.env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "..", "templates")))

    def send_email(self, subject: str, recipient: str, html_content: str):
        if not self.smtp_user or not self.smtp_pass:
            print("Mock sending email (No SMTP configured):")
            print(f"To: {recipient}")
            print(f"Subject: {subject}")
            print("Body:", html_content)
            return

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = recipient

        part = MIMEText(html_content, "html")
        msg.attach(part)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_pass)
            server.sendmail(self.smtp_user, recipient, msg.as_string())
            server.quit()
            print(f"Email sent successfully to {recipient}")
        except Exception as e:
            print(f"Error sending email to {recipient}: {str(e)}")

    def send_contact_emails(self, name: str, email: str, message: str, admin_email: str = "admin@nexconnect.com"):
        # Send user confirmation
        try:
            user_template = self.env.get_template("user_confirmation.html")
            user_html = user_template.render(name=name)
            self.send_email("Thank you for contacting NexConnect", email, user_html)
        except Exception as e:
            print(f"Failed to send user confirmation: {str(e)}")

        # Send admin alert
        try:
            admin_template = self.env.get_template("admin_alert.html")
            admin_html = admin_template.render(name=name, email=email, message=message)
            self.send_email("New Contact Submission", admin_email, admin_html)
        except Exception as e:
            print(f"Failed to send admin alert: {str(e)}")
