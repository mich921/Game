"""Модуль для работы с хранилищем задач"""

import csv
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

    def import_from_json(self, file_path: str) -> None:
        """
        Импортирует задачи из JSON-файла

        :param file_path: Путь к JSON-файлу с задачами
        :raises Exception: Если произошла ошибка при импорте
        """
        try:
            existing_tasks = self.load_tasks()

            with open(file_path, "r") as file:
                tasks_data = json.load(file)
                new_tasks = [Task.from_dict(task_data) for task_data in tasks_data]

            combined_tasks = existing_tasks + new_tasks
            self.save_tasks(combined_tasks)
        except Exception as e:
            raise Exception(f"Ошибка при импорте из JSON: {e}")

    def import_from_csv(self, file_path: str) -> None:
        """
        Импортирует задачи из CSV-файла

        :param file_path: Путь к CSV-файлу с задачами
        :raises Exception: Если произошла ошибка при импорте
        """
        try:
            existing_tasks = self.load_tasks()

            new_tasks = []
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    task = Task(
                        title=row["Title"],
                        description=row["Description"],
                        due_date=datetime.fromisoformat(row["Due Date"]),
                        priority=row["Priority"],
                        category=row["Category"],
                        status=row["Status"]
                    )
                    new_tasks.append(task)

            combined_tasks = existing_tasks + new_tasks
            self.save_tasks(combined_tasks)
        except Exception as e:
            raise Exception(f"Ошибка при импорте из CSV: {e}")

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
