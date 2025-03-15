# task_manager/task.py

from datetime import datetime


class Task:
    def __init__(self, title, description, due_date, priority, category, status="В работе"):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.category = category
        self.status = status
        self.created_at = datetime.now()

    def update_status(self, new_status):
        self.status = new_status

    def to_dict(self):
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
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=datetime.fromisoformat(data["due_date"]),
            priority=data["priority"],
            category=data["category"],
            status=data["status"]
        )