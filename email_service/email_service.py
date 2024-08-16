import yagmail
import keys.keys as keys


class EmailSenderService:
    def __init__(self):
        self.yag = yagmail.SMTP(keys.GMAIL_EMAIL, keys.GMAIL_APP_PASSWORD)

    def send_email(self, to_email, subject, html_content):
        try:
            response = self.yag.send(to=to_email, subject=subject, contents=html_content)
            print(f"Email sent to {to_email} with status code {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {e}")
