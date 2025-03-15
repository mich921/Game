# task_manager/email_notifier.py

import smtplib
from email.mime.text import MIMEText

class EmailNotifier:
    def __init__(self, email="your_email@yandex.ru", password="your_password"):
        self.email = email
        self.password = password

    def send_email(self, to_email, message):
        msg = MIMEText(message)
        msg["Subject"] = "Уведомление о задаче"
        msg["From"] = self.email
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.yandex.ru", 465) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, to_email, msg.as_string())