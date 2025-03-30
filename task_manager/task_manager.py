"""Модуль для управления задачами с использованием функций высшего порядка"""

import csv
import json
from datetime import date, datetime

from .task import Task
from .storage_abc import AbstractStorage


class TaskManager:
    """Класс для управления задачами с функциональным подходом"""

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

    def __update_tasks(self) -> None:
        """Полностью обновляет список задач"""
        self._tasks = self.storage.load_tasks().copy()

    def add_task(self, task: Task) -> None:
        """
        Добавляет новую задачу
        :param task: Объект задачи для добавления
        """
        tasks = self.tasks
        tasks.append(task)
        self.storage.save_tasks(tasks)
        self.__update_tasks()

    def edit_task(self, task_id: int, updated_task: Task) -> None:
        """
        Редактирует задачу по ID
        :param task_id: ID задачи для редактирования
        :param updated_task: Обновленный объект задачи
        :raises IndexError: Если ID задачи недопустим
        """
        if not (0 <= task_id < len(self.tasks)):
            raise IndexError("Недопустимый ID задачи")
        self.storage.edit_task(task_id, updated_task)
        self.__update_tasks()

    def delete_task(self, task_id: int) -> None:
        """
        Удаляет задачу по ID
        :param task_id: ID задачи для удаления
        :raises IndexError: Если ID задачи недопустим
        """
        if not (0 <= task_id < len(self.tasks)):
            raise IndexError("Недопустимый ID задачи")
        tasks = list(filter(lambda t: t != self.tasks[task_id], self.tasks))
        self.storage.save_tasks(tasks)
        self.__update_tasks()

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
        return list(filter(lambda task: task.status == status, self.tasks))

    def get_tasks_by_category(self, category: str) -> list[Task]:
        """
        Возвращает задачи по категории
        :param category: Категория задач для фильтрации
        :return: Список задач с указанной категорией
        """
        return list(filter(lambda task: task.category == category, self.tasks))

    def get_overdue_tasks(self) -> list[Task]:
        """
        Возвращает просроченные задачи
        :return: Список просроченных задач
        """
        now = date.today()
        return list(filter(
            lambda task: task.due_date < now and task.status != "Завершено",
            self.tasks
        ))

    def sort_tasks(self, tasks: list[Task], sort_by: str, reverse: bool = False) -> list[Task]:
        """
        Сортирует список задач по указанному критерию.

        :param tasks: Список задач для сортировки
        :param sort_by: Критерий сортировки (одна из констант SORT_*)
        :param reverse: Обратный порядок сортировки (по умолчанию False)
        :return: Отсортированный список задач
        :raises ValueError: Если передан неверный критерий сортировки
        """
        if sort_by and sort_by not in self.ALL_SORTS:
            raise ValueError(f"Недопустимый критерий сортировки: {sort_by}")

        if sort_by == self.SORT_TITLE:
            return sorted(tasks, key=lambda x: x.title, reverse=reverse)
        elif sort_by == self.SORT_DESCRIPTION:
            return sorted(tasks, key=lambda x: x.description, reverse=reverse)
        elif sort_by == self.SORT_DATE:
            return sorted(tasks, key=lambda x: x.due_date, reverse=reverse)
        elif sort_by == self.SORT_PRIORITY:
            return sorted(tasks, key=lambda x: Task.ALL_PRIORITIES.index(x.priority), reverse=reverse)
        elif sort_by == self.SORT_CATEGORY:
            return sorted(tasks, key=lambda x: x.category, reverse=reverse)
        elif sort_by == self.SORT_STATUS:
            return sorted(tasks, key=lambda x: Task.ALL_STATUSES.index(x.status), reverse=reverse)
        else:
            return tasks.copy()

    def import_from_json(self, file_path: str) -> None:
        """
        Импортирует задачи из JSON-файла и объединяет с текущими.

        :param file_path: Путь к JSON-файлу
        :raises Exception: Если импорт не удался
        """
        try:
            with open(file_path, "r") as file:
                tasks_data = json.load(file)
                new_tasks = [Task.from_dict(task_data) for task_data in tasks_data]

            combined_tasks = self.tasks + new_tasks
            self.storage.save_tasks(combined_tasks)
            self.__update_tasks()  # Обновляем кэш задач
        except Exception as e:
            raise Exception(f"Ошибка импорта из JSON: {e}")

    def import_from_csv(self, file_path: str) -> None:
        """
        Импортирует задачи из CSV-файла и объединяет с текущими.

        :param file_path: Путь к CSV-файлу
        :raises Exception: Если импорт не удался
        """
        try:
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

            combined_tasks = self.tasks + new_tasks
            self.storage.save_tasks(combined_tasks)
            self.__update_tasks()  # Обновляем кэш задач
        except Exception as e:
            raise Exception(f"Ошибка импорта из CSV: {e}")

    def search_tasks(self, keyword: str) -> list[Task]:
        """
        Ищет задачи по ключевому слову
        :param keyword: Ключевое слово для поиска
        :return: Список задач, содержащих ключевое слово
        """
        keyword = keyword.lower()
        return list(filter(
            lambda task: any(
                keyword in getattr(task, attr).lower()
                for attr in ['title', 'description', 'category', 'status']
            ),
            self.tasks
        ))
