"""Модуль для работы с хранилищем задач"""

import json
import os
from datetime import datetime

from .task import Task
from .storage_abc import AbstractStorage


class Storage(AbstractStorage):
    """Класс для работы с хранилищем задач"""

    def __init__(self, file_path: str = "data/tasks.json") -> None:
        """
        Инициализация хранилища

        :param file_path: Путь к файлу с задачами. По умолчанию "data/tasks.json"
        """
        self.file_path = file_path
        self.backup_dir = "data/backup"
        os.makedirs(self.backup_dir, exist_ok=True)

    def load_tasks(self) -> list[Task]:
        """
        Загружает задачи из JSON-файла

        :return: Список задач
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task_data) for task_data in tasks_data]
        return []

    def save_tasks(self, tasks: list[Task]) -> None:
        """
        Сохраняет задачи в JSON-файл

        :param tasks: Список задач для сохранения
        """
        with open(self.file_path, "w") as file:
            tasks_data = [task.to_dict() for task in tasks]
            json.dump(tasks_data, file, indent=4)
        self._create_backup()

    def edit_task(self, task_id: int, updated_task: Task) -> None:
        """
        Редактирует задачу по ID

        :param task_id: ID задачи для редактирования
        :param updated_task: Обновленный объект задачи
        :raises IndexError: Если ID задачи недопустим
        """
        tasks = self.load_tasks()

        if 0 <= task_id < len(tasks):
            tasks[task_id] = updated_task
            self.save_tasks(tasks)
        else:
            raise IndexError("Недопустимый ID задачи")

    def _create_backup(self) -> None:
        """
        Создает резервную копию данных, сохраняется в директорию `backup_dir`
        """
        backup_file = os.path.join(self.backup_dir, f"tasks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = file.read()
            with open(backup_file, "w") as backup:
                backup.write(data)
