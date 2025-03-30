"""Модуль для автоматической проверки дедлайнов задач"""

import schedule
import time
from datetime import datetime

from .storage import Storage
from .task_manager import TaskManager
from .email_notifier import EmailNotifier


def check_deadlines() -> None:
    """
    Проверяет задачи на наличие просроченных дедлайнов и отправляет уведомления
    Если задача просрочена и не завершена, отправляет уведомление на почту
    """
    storage = Storage()
    task_manager = TaskManager(storage)
    email_notifier = EmailNotifier()

    tasks = task_manager.get_tasks()
    now = datetime.now()

    for task in tasks:
        if task.due_date <= now and task.status != "Завершено":
            subject = f"Напоминание: Срок выполнения задачи '{task.title}'"
            message = (
                f"Заголовок: {task.title}\n"
                f"Описание: {task.description}\n"
                f"Срок выполнения: {task.due_date}\n"
                f"Категория: {task.category}\n"
                f"Приоритет: {task.priority}\n\n"
                "Пожалуйста, завершите задачу!"
            )
            email_notifier.send_email("pamagite@yandex.ru", subject, message)


def start_background_scheduler() -> None:
    """
    Запускает фоновый планировщик для проверки дедлайнов
    Планировщик проверяет задачи каждую минуту
    """
    # Проверка дедлайнов каждую минуту
    schedule.every(1).minutes.do(check_deadlines)

    # Запуск планировщика в бесконечном цикле
    while True:
        schedule.run_pending()
        time.sleep(1)
