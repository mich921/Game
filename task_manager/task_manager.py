from .storage import Storage
from datetime import date


class TaskManager:
    def __init__(self):
        self.storage = Storage()
        self.tasks = self.storage.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)

    def edit_task(self, task_id, new_task_data):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id] = new_task_data
            self.storage.save_tasks(self.tasks)
        else:
            raise IndexError("Task ID out of range")

    def delete_task(self, task_id):
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.storage.save_tasks(self.tasks)
        else:
            raise IndexError("Task ID out of range")

    def get_task(self, task_id):
        if 0 <= task_id < len(self.tasks):
            return self.tasks[task_id]
        else:
            raise IndexError("Task ID out of range")

    def get_tasks(self):
        return self.tasks

    def get_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_category(self, category):
        return [task for task in self.tasks if task.category == category]

    def get_overdue_tasks(self):
        today = date.today()
        return [task for task in self.tasks if task.due_date < today and task.status != "Завершено"]
