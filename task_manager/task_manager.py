"""Модуль для управления задачами"""

from datetime import date
from typing import Literal

from .task import Task
from .storage_abc import AbstractStorage


class TaskManager:
    """Класс для управления задачами"""

    SORT_TITLE = 'Title'
    SORT_DESCRIPTION = 'Description'
    SORT_DATE = 'Due Date'
    SORT_PRIORITY = 'Priority'
    SORT_CATEGORY = 'Category'
    SORT_STATUS = 'Status'

    ALL_SORTS = (SORT_TITLE, SORT_DESCRIPTION, SORT_DATE, SORT_PRIORITY, SORT_CATEGORY, SORT_STATUS)

    def __init__(self, storage: AbstractStorage) -> None:
        """Инициализация менеджера задач"""
        self.storage = storage
        self._tasks = self.storage.load_tasks()

    @property
    def tasks(self) -> list[Task]:
        """Возвращает копию списка задач для безопасности"""
        return self._tasks.copy()

    def update_tasks(self) -> None:
        """Полностью обновляет список задач"""
        self._tasks = self.storage.load_tasks().copy()

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
            self.update_tasks()
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
        now = date.today()
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
