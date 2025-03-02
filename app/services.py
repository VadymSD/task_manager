from functools import wraps

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.models import Task, db


class TaskNotFoundError(Exception):
    """Custom exception raised when a requested task is not found."""

    def __init__(self, task_id):
        """Initialize the exception with a task ID.

        Args:
            task_id (int): The ID of the task that was not found.

        Returns:
            None

        """
        self.message = f"Task with ID {task_id} not found."
        super().__init__(self.message)


def handle_db_errors(func):
    """Wrap database operations and handle SQLAlchemy errors.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function.

    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TaskNotFoundError:
            # Let TaskNotFoundError propagate.
            raise
        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception(f"Database error occurred in {func.__name__}")
            raise

    return wrapper


@handle_db_errors
def create_task(title, description, due_date):
    """Create a task object and add it to the database.

    Args:
        title (str): The title of the task.
        description (str): The description of the task.
        due_date (str): The due date of the task.

    Returns:
        Task: The created task object.

    """
    task = Task(title=title, description=description, due_date=due_date)
    db.session.add(task)
    db.session.commit()
    current_app.logger.info(f"Task with id {task.id} created successfully.")
    return task


@handle_db_errors
def list_tasks():
    """Retrieve all tasks from the database.

    Returns:
        list: A list of task objects.

    """
    tasks = db.session.scalars(db.select(Task)).all()
    current_app.logger.debug("Tasks retrieved successfully.")
    return tasks


@handle_db_errors
def complete_task(task_id):
    """Mark a task as completed.

    Args:
        task_id (int): The ID of the task to be completed.

    Returns:
        Task: The completed task object.

    Raises:
        TaskNotFoundError: If the task with the given ID is not found.

    """
    task = db.session.get(Task, task_id)
    if not task:
        current_app.logger.warning(f"Attempt to complete non-existent task: {task_id}")
        raise TaskNotFoundError(task_id)
    if task.completed:
        current_app.logger.warning(
            f"Attempt to complete already completed task: {task_id}"
        )
    else:
        task.completed = True
        db.session.commit()
        current_app.logger.info(f"Task '{task.title}' marked as complete.")
    return task


@handle_db_errors
def delete_task(task_id):
    """Delete a task from the database.

    Args:
        task_id (int): The ID of the task to be deleted.

    Returns:
        Task: The deleted task object.

    Raises:
        TaskNotFoundError: If the task with the given ID is not found.

    """
    task = db.session.get(Task, task_id)
    if not task:
        current_app.logger.warning(f"Attempt to delete a non-existent task: {task_id}")
        raise TaskNotFoundError(task_id)
    db.session.delete(task)
    db.session.commit()
    current_app.logger.info(f"Task '{task.title}' deleted successfully.")
    return task
