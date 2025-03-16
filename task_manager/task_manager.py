# task_manager/task_manager.py

from .storage import Storage
from .task import Task

class TaskManager:
    def __init__(self):
        self.storage = Storage()
        self.tasks = self.storage.load_tasks()

    def add_task(self, task):
        """Добавление новой задачи."""
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)

    def edit_task(self, task_id, updated_task):
        """Редактирование задачи по ID."""
        if 0 <= task_id < len(self.tasks):
            self.storage.edit_task(task_id, updated_task)  # Используем метод Storage для редактирования
            self.tasks = self.storage.load_tasks()  # Обновляем локальный список задач
        else:
            raise IndexError("Недопустимый ID задачи")

    def delete_task(self, task_id):
        """Удаление задачи по ID."""
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.storage.save_tasks(self.tasks)
        else:
            raise IndexError("Недопустимый ID задачи")

    def get_task(self, task_id):
        """Получение задачи по ID."""
        if 0 <= task_id < len(self.tasks):
            return self.tasks[task_id]
        else:
            raise IndexError("Недопустимый ID задачи")

    def get_tasks(self):
        """Получение списка всех задач."""
        return self.tasks

    def get_tasks_by_status(self, status):
        """Получение задач по статусу."""
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_category(self, category):
        """Получение задач по категории."""
        return [task for task in self.tasks if task.category == category]

    def get_overdue_tasks(self):
        """Получение просроченных задач."""
        from datetime import datetime
        now = datetime.now()
        return [task for task in self.tasks if task.due_date < now and task.status != "Завершено"]

    def search_tasks(self, keyword):
        """Поиск задач по ключевому слову."""
        keyword = keyword.lower()
        return [
            task for task in self.tasks
            if (keyword in task.title.lower() or
                keyword in task.description.lower() or
                keyword in task.category.lower() or
                keyword in task.status.lower())
        ]