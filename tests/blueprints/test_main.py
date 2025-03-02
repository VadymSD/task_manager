from unittest.mock import patch

import pytest
from sqlalchemy.exc import SQLAlchemyError


def test_index_get(client):
    """Test the main page rendering.

    Args:
        client (FlaskClient): The Flask test client.

    Returns:
        None

    """
    response = client.get("/")
    assert response.status_code == 200
    assert b'<h2 class="mb-3">Create a New Task</h2>' in response.get_data()
    assert b'<h1 class="text-center mb-4">Task Manager</h1>' in response.get_data()


@pytest.mark.parametrize(
    "task_data",
    [
        {
            "title": "Param Title 1",
            "description": "Param Desc 1",
            "due_date": "2030-01-01",
        },
        {
            "title": "Param Title 2",
            "description": "Param Desc 2",
            "due_date": "2031-01-01",
        },
    ],
)
def test_index_post(create_task_via_route, task_data):
    """Test the task creation via POST request.

    Args:
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    response = create_task_via_route(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )
    assert response.status_code == 200
    response_text = response.get_data(as_text=True)
    assert task_data["title"] in response_text
    assert task_data["description"] in response_text
    assert task_data["due_date"] in response_text


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
def test_index_db_error(create_task_via_route, task_data):
    """Test the task creation with database error.

    Args:
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    with patch("app.models.db.session.commit") as mock_commit:
        mock_commit.side_effect = SQLAlchemyError("Simulated DB error")

        response = create_task_via_route(
            title=task_data["title"],
            description=task_data["description"],
            due_date=task_data["due_date"],
        )

        assert b"The database error has happened." in response.data


@pytest.mark.parametrize(
    "task_data",
    [
        {
            "title": "Param Title 1",
            "description": "Param Desc 1",
            "due_date": "2030-01-01",
        },
        {
            "title": "Param Title 2",
            "description": "Param Desc 2",
            "due_date": "2031-01-01",
        },
    ],
)
def test_complete_task_route_success(client, create_task_via_route, task_data):
    """Test the task completion via POST request.

    Args:
        client (FlaskClient): The Flask test client.
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    create_task_via_route(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )

    response = client.post("/complete_task/1", follow_redirects=True)
    assert (
        b'<button type="submit" class="btn btn-success btn-sm">Complete</button>'
        not in response.get_data()
    )
    assert response.status_code == 200
    response_text = response.get_data(as_text=True)
    assert "Completed" in response_text


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
def test_complete_task_route_task_not_found_error(
    client, create_task_via_route, task_data
):
    """Test the task completion with task not found error.

    Args:
        client (FlaskClient): The Flask test client.
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    create_task_via_route(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )

    response = client.post("/complete_task/1234", follow_redirects=True)
    assert b"Task not found or already completed." in response.data


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
def test_complete_task_route_db_error(client, create_task_via_route, task_data):
    """Test the task completion with database error.

    Args:
        client (FlaskClient): The Flask test client.
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    create_task_via_route(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )

    with patch("app.models.db.session.commit") as mock_commit:
        mock_commit.side_effect = SQLAlchemyError("Simulated DB error")

        response = client.post("/complete_task/1", follow_redirects=True)
        assert b"The database error has happened." in response.data


@pytest.mark.parametrize(
    "task_data",
    [
        {
            "title": "Param Title 1",
            "description": "Param Desc 1",
            "due_date": "2030-01-01",
        },
        {
            "title": "Param Title 2",
            "description": "Param Desc 2",
            "due_date": "2031-01-01",
        },
    ],
)
def test_delete_task_route_success(client, create_task_via_route, task_data):
    """Test the task deletion via POST request.

    Args:
        client (FlaskClient): The Flask test client.
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    create_task_via_route(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )

    response = client.post("/delete_task/1", follow_redirects=True)
    assert response.status_code == 200
    response_text = response.get_data(as_text=True)
    assert task_data["description"] not in response_text
    assert task_data["due_date"] not in response_text
    assert f"Task {task_data['title']}" in response_text


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
def test_delete_task_route_task_not_found_error(
    client, create_task_via_route, task_data
):
    """Test the task deletion with task not found error.

    Args:
        client (FlaskClient): The Flask test client.
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    create_task_via_route(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )

    response = client.post("/delete_task/1234", follow_redirects=True)
    assert b"Task not found or already deleted." in response.data


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
def test_delete_task_route_db_error(client, create_task_via_route, task_data):
    """Test the task deletion with database error.

    Args:
        client (FlaskClient): The Flask test client.
        create_task_via_route (function): The function to create a task via route.
        task_data (dict): The task data.

    Returns:
        None

    """
    create_task_via_route(
        title=task_data["title"],
        description=task_data["description"],
        due_date=task_data["due_date"],
    )

    with patch("app.models.db.session.commit") as mock_commit:
        mock_commit.side_effect = SQLAlchemyError("Simulated DB error")

        response = client.post("/delete_task/1", follow_redirects=True)
        assert b"The database error has happened." in response.data
