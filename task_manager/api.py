"""Модуль для API взаимодействия с задачами"""

from flask import Flask, jsonify, request
from datetime import datetime
from typing import Any

from .task import Task
from .storage import Storage
from .task_manager import TaskManager


app = Flask(__name__)


class TaskAPI:
    """Класс для обработки API запросов, связанных с задачами"""

    def __init__(self) -> None:
        """Инициализация API для работы с задачами"""
        storage = Storage()
        self.task_manager = TaskManager(storage)

    def task_to_dict(self, task: Task) -> dict[str, Any]:
        """
        Преобразует задачу в словарь

        :param task: Объект задачи
        :return: Словарь с данными задачи
        """
        return {
            "id": id(task),
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat(),
            "priority": task.priority,
            "category": task.category,
            "status": task.status,
            "created_at": task.created_at.isoformat()
        }

    def get_tasks(self) -> jsonify:
        """
        Возвращает список задач с возможностью сортировки

        :return: JSON-ответ с отсортированным списком задач
        """
        sort_column = request.args.get("sort_by", default=None)
        sort_order = request.args.get("order", default=False)

        tasks = self.task_manager.get_tasks()

        sorted_tasks = self.task_manager.sort_tasks(tasks, sort_column, sort_order)

        return jsonify([self.task_to_dict(task) for task in sorted_tasks])

    def add_task(self) -> jsonify:
        """
        Добавляет новую задачу

        :return: JSON-ответ с результатом операции
        """
        data = request.json
        try:
            new_task = Task(
                title=data["title"],
                description=data["description"],
                due_date=datetime.fromisoformat(data["due_date"]),
                priority=data["priority"],
                category=data["category"],
                status=data.get("status", "В работе")
            )
            self.task_manager.add_task(new_task)
            return jsonify({"status": "success", "message": "Задача добавлена"}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    def edit_task(self, task_id: int) -> jsonify:
        """
        Редактирует задачу по ID

        :param task_id: ID задачи для редактирования
        :return: JSON-ответ с результатом операции
        """
        data = request.json
        try:
            updated_task = Task(
                title=data["title"],
                description=data["description"],
                due_date=datetime.fromisoformat(data["due_date"]),
                priority=data["priority"],
                category=data["category"],
                status=data["status"]
            )
            self.task_manager.edit_task(task_id, updated_task)
            return jsonify({"status": "success", "message": "Задача обновлена"})
        except IndexError:
            return jsonify({"status": "error", "message": "Задача не найдена"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    def delete_task(self, task_id: int) -> jsonify:
        """
        Удаляет задачу по ID

        :param task_id: ID задачи для удаления
        :return: JSON-ответ с результатом операции
        """
        try:
            self.task_manager.delete_task(task_id)
            return jsonify({"status": "success", "message": "Задача удалена"})
        except IndexError:
            return jsonify({"status": "error", "message": "Задача не найдена"}), 404

    def get_completed_tasks(self) -> jsonify:
        """
        Возвращает список завершенных задач

        :return: JSON-ответ с завершенными задачами
        """
        completed_tasks = self.task_manager.get_tasks_by_status("Завершено")
        return jsonify([self.task_to_dict(task) for task in completed_tasks])

    def get_overdue_tasks(self) -> jsonify:
        """
        Возвращает список просроченных задач

        :return: JSON-ответ с просроченными задачами
        """
        overdue_tasks = self.task_manager.get_overdue_tasks()
        return jsonify([self.task_to_dict(task) for task in overdue_tasks])

    def visualize_tasks(self) -> jsonify:
        """
        Возвращает данные для визуализации задач по критерию

        :return: JSON-ответ с данными для визуализации
        """
        criteria = request.args.get("criteria", "category")
        tasks = self.task_manager.get_tasks()

        data = {}
        if criteria == "category":
            all_values = Task.ALL_CATEGORIES
        elif criteria == "priority":
            all_values = Task.ALL_PRIORITIES
        elif criteria == "status":
            all_values = Task.ALL_STATUSES
        else:
            return jsonify({"status": "error", "message": "Недопустимый критерий"}), 400

        for value in all_values:
            data[value] = 0

        for task in tasks:
            key = None
            if criteria == "category":
                key = task.category
            elif criteria == "priority":
                key = task.priority
            elif criteria == "status":
                key = task.status

            if key in data:
                data[key] += 1

        return jsonify({"criteria": criteria, "data": data})


# Создание экземпляра API
task_api = TaskAPI()


# Настройка маршрутов
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return task_api.get_tasks()


@app.route("/tasks", methods=["POST"])
def add_task():
    return task_api.add_task()


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    return task_api.edit_task(task_id)


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    return task_api.delete_task(task_id)


@app.route("/tasks/completed", methods=["GET"])
def get_completed_tasks():
    return task_api.get_completed_tasks()


@app.route("/tasks/overdue", methods=["GET"])
def get_overdue_tasks():
    return task_api.get_overdue_tasks()


@app.route("/tasks/visualize", methods=["GET"])
def visualize_tasks():
    return task_api.visualize_tasks()


if __name__ == "__main__":
    app.run(debug=True)
