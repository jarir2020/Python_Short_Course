"""Flask URL registration for task controllers."""

from flask import Blueprint, jsonify

from ..controllers import create_task, delete_task, get_task, list_tasks, update_task


task_api = Blueprint("task_api", __name__)


@task_api.get("/health")
def health():
    return jsonify(status="ok", framework="flask")


@task_api.get("/tasks")
def list_tasks_route():
    return jsonify([task.to_dict() for task in list_tasks()])


@task_api.post("/tasks")
def create_task_route():
    task = create_task()
    return jsonify(task.to_dict()), 201


@task_api.get("/tasks/<int:task_id>")
def get_task_route(task_id: int):
    task = get_task(task_id)
    if task is None:
        return jsonify(error="not_found", message="Task not found"), 404
    return jsonify(task.to_dict())


@task_api.patch("/tasks/<int:task_id>")
def update_task_route(task_id: int):
    task = update_task(task_id)
    if task is None:
        return jsonify(error="not_found", message="Task not found"), 404
    return jsonify(task.to_dict())


@task_api.delete("/tasks/<int:task_id>")
def delete_task_route(task_id: int):
    if not delete_task(task_id):
        return jsonify(error="not_found", message="Task not found"), 404
    return "", 204
