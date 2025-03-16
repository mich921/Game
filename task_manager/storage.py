# task_manager/storage.py

import json
import os
from datetime import date
from .task import Task


class Storage:
    def __init__(self, file_path="data/tasks.json"):
        self.file_path = file_path
        self.backup_dir = "data/backup"
        os.makedirs(self.backup_dir, exist_ok=True)

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task_data) for task_data in tasks_data]
        return []

    def save_tasks(self, tasks):
        with open(self.file_path, "w") as file:
            tasks_data = [task.to_dict() for task in tasks]
            json.dump(tasks_data, file, indent=4)
        self._create_backup()

    def _create_backup(self):
        backup_file = os.path.join(self.backup_dir, f"tasks_backup_{date.today().strftime('%Y%m%d')}.json")
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = file.read()
            with open(backup_file, "w") as backup:
                backup.write(data)