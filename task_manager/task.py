"""Модуль для работы с задачами"""

from dataclasses import dataclass
from datetime import date
from typing import ClassVar


@dataclass(frozen=True)
class Task:
    """
    Иммутабельный класс задачи.
    Все изменения создают новый экземпляр.
    """
    title: str
    description: str
    due_date: date
    priority: str = "Средний"
    category: str = "Работа"
    status: str = "В работе"
    created_at: date = date.today()

    DEFAULT_STATUS = 'В работе'
    DEFAULT_PRIORITY = 'Средний'
    DEFAULT_CATEGORY = 'Работа'

    # Константы класса
    ALL_CATEGORIES: ClassVar[list[str]] = ["Работа", "Личное", "Учеба"]
    ALL_PRIORITIES: ClassVar[list[str]] = ["Низкий", "Средний", "Высокий"]
    ALL_STATUSES: ClassVar[list[str]] = ["В работе", "Завершено"]

    def to_dict(self) -> dict:
        """Сериализация в словарь"""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Десериализация из словаря"""
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=date.fromisoformat(data["due_date"]),
            priority=data.get("priority", cls.DEFAULT_PRIORITY),
            category=data.get("category", cls.DEFAULT_CATEGORY),
            status=data.get("status", cls.DEFAULT_STATUS)
        )
