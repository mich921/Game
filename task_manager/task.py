"""Модуль для работы с задачами"""

from datetime import date, datetime


class Task:
    """
    Класс, представляющий задачу.
    """

    DEFAULT_STATUS = 'В работе'
    DEFAULT_PRIORITY = 'Средний'
    DEFAULT_CATEGORY = 'Работа'

    ALL_CATEGORIES = ["Работа", "Личное", "Учеба"]
    ALL_PRIORITIES = ["Низкий", "Средний", "Высокий"]
    ALL_STATUSES = ["В работе", "Завершено"]

    def __init__(
            self, title: str, description: str, due_date: date,
            priority: str = DEFAULT_PRIORITY, category: str = DEFAULT_CATEGORY, status: str = DEFAULT_STATUS
    ) -> None:
        """
        Инициализация задачи

        :param title: Заголовок задачи
        :param description: Описание задачи
        :param due_date: Срок выполнения задачи
        :param priority: Приоритет задачи. По умолчанию "Средний"
        :param category: Категория задачи. По умолчанию "Работа"
        :param status: Статус задачи. По умолчанию "В работе"
        """
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.status = status
        self.created_at = date.today()

    def to_dict(self) -> dict[str, date | str | None]:
        """
        Преобразует задачу в словарь

        :return: Словарь с данными задачи
        """
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "created_at": datetime.now().isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict[str, date | str | None]) -> 'Task':
        """
        Создает задачу из словаря

        :param data: Словарь с данными задачи
        :return: Объект задачи
        """
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=date.fromisoformat(data["due_date"]),
            priority=data["priority"],
            category=data["category"],
            status=data["status"]
        )
