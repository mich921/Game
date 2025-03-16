"""Модуль для отправки уведомлений по электронной почте"""

import smtplib
from email.mime.text import MIMEText


class EmailNotifier:
    """Класс для отправки уведомлений по электронной почте"""

    def __init__(self, email: str = "mich921@yandex.ru", password: str = "password") -> None:
        """
        Инициализация уведомителя

        :param email: Адрес электронной почты отправителя. По умолчанию "mich921@yandex.ru"
        :param password: Пароль от почтового аккаунта. По умолчанию "password"
        """
        self.email = email
        self.password = password

    def send_email(self, to_email: str, subject: str, message: str) -> None:
        """
        Отправляет электронное письмо

        :param to_email: Адрес электронной почты получателя
        :param subject: Тема письма
        :param message: Текст письма
        """
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
