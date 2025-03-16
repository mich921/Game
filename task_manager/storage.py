# task_manager/storage.py
import csv
import json
import os
from datetime import datetime
from .task import Task


class Storage:
    def __init__(self, file_path="data/tasks.json"):
        self.file_path = file_path
        self.backup_dir = "data/backup"
        os.makedirs(self.backup_dir, exist_ok=True)

    def load_tasks(self):
        """Загрузка задач из JSON-файла."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task_data) for task_data in tasks_data]
        return []

    def save_tasks(self, tasks):
        """Сохранение задач в JSON-файл."""
        with open(self.file_path, "w") as file:
            tasks_data = [task.to_dict() for task in tasks]
            json.dump(tasks_data, file, indent=4)
        self._create_backup()

    def edit_task(self, task_id, updated_task):
        """Редактирование конкретной задачи."""
        tasks = self.load_tasks()

        # Проверка, что task_id находится в допустимом диапазоне
        if 0 <= task_id < len(tasks):
            tasks[task_id] = updated_task  # Обновление задачи
            self.save_tasks(tasks)  # Сохранение изменений
        else:
            raise IndexError("Недопустимый ID задачи")

    def import_from_json(self, file_path):
        """Импорт задач из JSON-файла."""
        with open(file_path, "r") as file:
            tasks_data = json.load(file)
            tasks = [Task.from_dict(task_data) for task_data in tasks_data]
            self.save_tasks(tasks)

    def import_from_csv(self, file_path):
        """Импорт задач из CSV-файла."""
        tasks = []
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
                tasks.append(task)
        self.save_tasks(tasks)

    def _create_backup(self):
        """Создание резервной копии данных."""
        backup_file = os.path.join(self.backup_dir, f"tasks_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = file.read()
            with open(backup_file, "w") as backup:
                backup.write(data)