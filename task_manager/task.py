# task_manager/task.py

from datetime import date, datetime


class Task:
    """Класс для работы "Задачами" """
    DEFAULT_STATUS = 'В работе'
    DEFAULT_PRIORITY = 'Средний'
    DEFAULT_CATEGORY = 'Работа'

    ALL_CATEGORIES = ["Работа", "Личное", "Учеба"]
    ALL_PRIORITIES = ["Низкий", "Средний", "Высокий"]
    ALL_STATUSES = ["В работе", "Завершено"]

    def __init__(
            self, title: str, description: str, due_date: date,
            priority=DEFAULT_PRIORITY, category=DEFAULT_CATEGORY, status=DEFAULT_STATUS
    ):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.status = status
        self.today = date.today()

    def to_dict(self):
        """Преобразование к словарю"""
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
    def from_dict(cls, data):
        """Преобразование из словаря"""
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=date.fromisoformat(data["due_date"]),
            priority=data["priority"],
            category=data["category"],
            status=data["status"]
        )
