from abc import ABC, abstractmethod

from .task import Task


class AbstractStorage(ABC):
    """Абстрактный класс для работы с данными"""

    @abstractmethod
    def load_tasks(self) -> list[Task]:
        pass

    @abstractmethod
    def save_tasks(self, tasks: list[Task]) -> None:
        pass

    @abstractmethod
    def edit_task(self, task_id: int, updated_task: Task) -> None:
        pass
