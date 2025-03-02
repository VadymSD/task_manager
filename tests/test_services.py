from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import Task
from app.services import (
    TaskNotFoundError,
    complete_task,
    create_task,
    delete_task,
    list_tasks,
)


def test_decorator_handle_db_errors_task_not_found_error(client):
    """Test the decorator that handles database errors for task not found.

    Args:
        client (FlaskClient): The Flask test client.

    Returns:
        None

    """
    with patch("app.models.db.session.scalars") as mock_scalars:
        mock_scalars.side_effect = TaskNotFoundError(1)
        with pytest.raises(TaskNotFoundError):
            list_tasks()


def test_decorator_handle_db_errors_sqlalchemy_error(client):
    """Test the decorator that handles SQLAlchemy errors.

    Args:
        client (FlaskClient): The Flask test client.

    Returns:
        None

    """
    db.session = MagicMock()
    with patch("app.models.db.session.scalars") as mock_scalars:
        mock_scalars.side_effect = SQLAlchemyError("Simulated SQLAlchemy error")
        with pytest.raises(SQLAlchemyError):
            list_tasks()
    db.session.rollback.assert_called_once()


@pytest.mark.parametrize(
    "task_data",
    [
        {
            "title": "Param Title 1",
            "description": "Param Desc 1",
            "due_date": "2030-01-01",
        },
    ],
)
def test_create_task_task(client, task_data):
    """Test the create_task function.

    Args:
        client (FlaskClient): The Flask test client.
        task_data (dict): The task data to be used for creating the task.

    Returns:
        None

    """
    db.session = MagicMock()
    test_task = create_task(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )
    assert test_task.title == task_data["title"]
    assert test_task.description == task_data["description"]
    assert test_task.due_date == task_data["due_date"]
    db.session.add.assert_called_once()
    db.session.commit.assert_called_once()


@pytest.mark.parametrize(
    "task_data",
    [
        {
            "title": "Param Title 1",
            "description": "Param Desc 1",
            "due_date": datetime(2030, 12, 11),
        },
    ],
)
def test_list_tasks(client, task_data, create_task_fixture):
    """Test the list_tasks function.

    Args:
        client (FlaskClient): The Flask test client.
        task_data (dict): The task data to be used for creating the task.
        create_task_fixture (function): The fixture to create a task.

    Returns:
        None

    """
    db.session = MagicMock()
    test_task = create_task_fixture(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )
    db.session.scalars.return_value.all.return_value = [test_task]
    test_tasks = list_tasks()
    db.session.scalars.assert_called_once()
    assert test_task in test_tasks


@pytest.mark.parametrize(
    "task_data",
    [
        {
            "title": "Param Title 1",
            "description": "Param Desc 1",
            "due_date": datetime(2030, 12, 11),
        },
    ],
)
def test_complete_task(client, task_data, create_task_fixture):
    """Test the complete_task function.

    Args:
        client (FlaskClient): The Flask test client.
        task_data (dict): The task data to be used for creating the task.
        create_task_fixture (function): The fixture to create a task.

    Returns:
        None

    """
    db.session = MagicMock()
    test_task = create_task_fixture(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )
    db.session.get.return_value = test_task
    completed_task = complete_task(test_task.id)
    db.session.get.assert_called_once_with(Task, test_task.id)
    assert completed_task.completed


@pytest.mark.parametrize(
    "task_data",
    [
        {
            "title": "Param Title 1",
            "description": "Param Desc 1",
            "due_date": datetime(2030, 12, 11),
        },
    ],
)
def test_delete_task(client, task_data, create_task_fixture):
    """Test the delete_task function.

    Args:
        client (FlaskClient): The Flask test client.
        task_data (dict): The task data to be used for creating the task.
        create_task_fixture (function): The fixture to create a task.

    Returns:
        None

    """
    db.session = MagicMock()
    test_task = create_task_fixture(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )
    db.session.get.return_value = test_task
    delete_task(test_task.id)
    db.session.get.assert_called_once_with(Task, test_task.id)
    db.session.delete.assert_called_once_with(test_task)
