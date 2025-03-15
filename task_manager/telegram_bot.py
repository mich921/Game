# task_manager/telegram_bot.py

import requests

class TelegramBot:
    def __init__(self, token="your_telegram_bot_token"):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id, text):
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        requests.post(url, json=payload)