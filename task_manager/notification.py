# task_manager/notification.py

from email_notifier import EmailNotifier
from telegram_bot import TelegramBot


class Notification:
    def __init__(self):
        self.email_notifier = EmailNotifier()
        self.telegram_bot = TelegramBot()

    def send_notification(self, message, user):
        self.email_notifier.send_email(user.email, message)
        self.telegram_bot.send_message(user.telegram_chat_id, message)