import smtplib
from email.mime.text import MIMEText


class EmailNotifier:
    def __init__(self, email="mich921@yandex.ru", password="password"):
        self.email = email
        self.password = password

    def send_email(self, to_email, subject, message):
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = to_email

        try:
            with smtplib.SMTP_SSL("smtp.yandex.ru", 465) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, to_email, msg.as_string())
            print(f"Уведомление отправлено на {to_email}")
        except Exception as e:
            print(f"Ошибка при отправке уведомления: {e}")