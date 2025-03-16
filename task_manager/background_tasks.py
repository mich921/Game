# task_manager/background_tasks.py

import schedule
import time
from datetime import datetime
from .task_manager import TaskManager
from .email_notifier import EmailNotifier


def check_deadlines():
    task_manager = TaskManager()
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


def start_background_scheduler():
    # Проверка дедлайнов каждую минуту (можно изменить на schedule.every().hour и т.д.)
    schedule.every(1).minutes.do(check_deadlines)

    # Запуск планировщика в бесконечном цикле
    while True:
        schedule.run_pending()
        time.sleep(1)