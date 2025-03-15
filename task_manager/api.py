# task_manager/api.py

from flask import Flask, jsonify, request
from .task_manager import TaskManager

app = Flask(__name__)
task_manager = TaskManager()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = task_manager.get_tasks()
    return jsonify([task.to_dict() for task in tasks])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task = Task(
        title=data["title"],
        description=data["description"],
        due_date=datetime.fromisoformat(data["due_date"]),
        priority=data["priority"],
        category=data["category"]
    )
    task_manager.add_task(task)
    return jsonify({"status": "success"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.json
    task = Task(
        title=data["title"],
        description=data["description"],
        due_date=datetime.fromisoformat(data["due_date"]),
        priority=data["priority"],
        category=data["category"],
        status=data["status"]
    )
    task_manager.edit_task(task_id, task)
    return jsonify({"status": "success"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task_manager.delete_task(task_id)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)