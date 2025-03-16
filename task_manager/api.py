# task_manager/api.py

from flask import Flask, jsonify, request
from datetime import datetime
from .task_manager import TaskManager
from .task import Task


app = Flask(__name__)
task_manager = TaskManager()


# Вспомогательная функция для преобразования задачи в словарь
def __task_to_dict(task):
    return {
        "id": id(task),  # Уникальный идентификатор задачи (временное решение)
        "title": task.title,
        "description": task.description,
        "due_date": task.due_date.isoformat(),
        "priority": task.priority,
        "category": task.category,
        "status": task.status,
        "created_at": task.created_at.isoformat()
    }


# Получение списка всех задач
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = task_manager.get_tasks()
    return jsonify([__task_to_dict(task) for task in tasks])


# Добавление новой задачи
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    try:
        new_task = Task(
            title=data["title"],
            description=data["description"],
            due_date=datetime.fromisoformat(data["due_date"]),
            priority=data["priority"],
            category=data["category"],
            status=data.get("status", "В работе")  # По умолчанию "В работе"
        )
        task_manager.add_task(new_task)
        return jsonify({"status": "success", "message": "Задача добавлена"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# Редактирование задачи по ID
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
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
        task_manager.edit_task(task_id, updated_task)
        return jsonify({"status": "success", "message": "Задача обновлена"})
    except IndexError:
        return jsonify({"status": "error", "message": "Задача не найдена"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# Удаление задачи по ID
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task_manager.delete_task(task_id)
        return jsonify({"status": "success", "message": "Задача удалена"})
    except IndexError:
        return jsonify({"status": "error", "message": "Задача не найдена"}), 404


# Получение отчета по выполненным задачам
@app.route("/tasks/completed", methods=["GET"])
def get_completed_tasks():
    completed_tasks = [task for task in task_manager.get_tasks() if task.status == "Завершено"]
    return jsonify([__task_to_dict(task) for task in completed_tasks])


# Получение отчета по просроченным задачам
@app.route("/tasks/overdue", methods=["GET"])
def get_overdue_tasks():
    overdue_tasks = task_manager.get_overdue_tasks()
    return jsonify([__task_to_dict(task) for task in overdue_tasks])


# Визуализация данных (возвращает данные для построения графика)
@app.route("/tasks/visualize", methods=["GET"])
def visualize_tasks():
    criteria = request.args.get("criteria", "category")  # По умолчанию "category"
    tasks = task_manager.get_tasks()

    # Подсчет данных в зависимости от критерия
    data = {}
    if criteria == "category":
        all_values = Task.ALL_CATEGORIES
    elif criteria == "priority":
        all_values = Task.ALL_PRIORITIES
    elif criteria == "status":
        all_values = Task.ALL_STATUSES
    else:
        return jsonify({"status": "error", "message": "Недопустимый критерий"}), 400

    # Инициализация данных нулевыми значениями
    for value in all_values:
        data[value] = 0

    # Подсчет задач
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


if __name__ == "__main__":
    app.run(debug=True)
