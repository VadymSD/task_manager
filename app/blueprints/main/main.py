# app/main.py
from flask import Blueprint, flash, redirect, render_template, url_for
from sqlalchemy.exc import SQLAlchemyError

from app.forms import TaskForm
from app.services import (
    TaskNotFoundError,
    complete_task,
    create_task,
    delete_task,
    list_tasks,
)

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def index():
    """Render the main page with a task form and list of tasks.

    Returns:
        str: Rendered HTML template for the main page.

    """
    form = TaskForm()
    tasks = []
    try:
        if form.validate_on_submit():
            create_task(form.title.data, form.description.data, form.due_date.data)
        tasks = list_tasks()
    except SQLAlchemyError:
        flash("The database error has happened.")
    return render_template("index.html", form=form, tasks=tasks)


@main_bp.route("/complete_task/<int:task_id>", methods=["POST"])
def complete_task_route(task_id):
    """Mark a task as complete.

    Args:
        task_id (int): The ID of the task to be marked as complete.

    Returns:
        str: Redirect to the main page.

    """
    try:
        task = complete_task(task_id)  # call to service
        flash(f"Task {task.title} marked as complete.")
    except TaskNotFoundError:
        flash("Task not found or already completed.")
    except SQLAlchemyError:
        flash("The database error has happened.")
    return redirect(url_for("main_bp.index"))


@main_bp.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task_route(task_id):
    """Delete a task.

    Args:
        task_id (int): The ID of the task to be deleted.

    Returns:
        str: Redirect to the main page.

    """
    try:
        task = delete_task(task_id)
        flash(f"Task {task.title} was deleted.")
    except TaskNotFoundError:
        flash("Task not found or already deleted.")
    except SQLAlchemyError:
        flash("The database error has happened.")
    return redirect(url_for("main_bp.index"))
