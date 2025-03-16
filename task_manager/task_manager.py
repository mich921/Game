"""Модуль для управления задачами"""

from datetime import datetime

from .storage import Storage
from .task import Task


class TaskManager:
    """Класс для управления задачами"""

    def __init__(self) -> None:
        """Инициализация менеджера задач"""
        self.storage = Storage()
        self.tasks = self.storage.load_tasks()

    def add_task(self, task: Task) -> None:
        """
        Добавляет новую задачу

        :param task: Объект задачи для добавления
        """
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)

    def edit_task(self, task_id: int, updated_task: Task) -> None:
        """
        Редактирует задачу по ID

        :param task_id: ID задачи для редактирования
        :param updated_task: Обновленный объект задачи
        :raises IndexError: Если ID задачи недопустим
        """
        if 0 <= task_id < len(self.tasks):
            self.storage.edit_task(task_id, updated_task)
            self.tasks = self.storage.load_tasks()
        else:
            raise IndexError("Недопустимый ID задачи")

    def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу по ID

        :param task_id: ID задачи для удаления
        :raises IndexError: Если ID задачи недопустим
        """
        if 0 <= task_id < len(self.tasks):
            del self.tasks[task_id]
            self.storage.save_tasks(self.tasks)
        else:
            raise IndexError("Недопустимый ID задачи")

    def get_task(self, task_id: int) -> Task:
        """
        Возвращает задачу по ID

        :param task_id: ID задачи
        :return: Объект задачи
        :raises IndexError: Если ID задачи недопустим
        """
        if 0 <= task_id < len(self.tasks):
            return self.tasks[task_id]
        else:
            raise IndexError("Недопустимый ID задачи")

    def get_tasks(self) -> list[Task]:
        """
        Возвращает список всех задач

        :return: Список задач
        """
        return self.tasks

    def get_tasks_by_status(self, status: str) -> list[Task]:
        """
        Возвращает задачи по статусу

        :param status: Статус задач для фильтрации
        :return: Список задач с указанным статусом
        """
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_category(self, category: str) -> list[Task]:
        """
        Возвращает задачи по категории

        :param category: Категория задач для фильтрации
        :return: Список задач с указанной категорией
        """
        return [task for task in self.tasks if task.category == category]

    def get_overdue_tasks(self) -> list[Task]:
        """
        Возвращает просроченные задачи

        :return: Список просроченных задач
        """
        now = datetime.now()
        return [task for task in self.tasks if task.due_date < now and task.status != "Завершено"]

    def search_tasks(self, keyword: str) -> list[Task]:
        """
        Ищет задачи по ключевому слову

        :param keyword: Ключевое слово для поиска
        :return: Список задач, содержащих ключевое слово
        """
        keyword = keyword.lower()
        return [
            task for task in self.tasks
            if (keyword in task.title.lower() or
                keyword in task.description.lower() or
                keyword in task.category.lower() or
                keyword in task.status.lower())
        ]
