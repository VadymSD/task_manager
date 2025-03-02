import pytest

from app import create_app, db
from app.services import create_task


@pytest.fixture()
def app():
    """Create a Flask application for the tests.

    Returns:
        Flask: The Flask application.

    """
    config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    }
    app = create_app(config_object=config)

    with app.app_context():
        db.create_all()  # Create all tables
        yield app
        db.drop_all()  # Drop all tables


@pytest.fixture()
def client(app):
    """Create a test client for the app.

    Args:
        app (Flask): The Flask application fixture.

    Returns:
        FlaskClient: The Flask test client.

    """
    return app.test_client()


@pytest.fixture()
def runner(app):
    """Create a test runner for the app.

    Args:
        app (Flask): The Flask application fixture.

    Returns:
        FlaskCliRunner: The Flask CLI test runner.

    """
    return app.test_cli_runner()


@pytest.fixture
def create_task_fixture():
    """Create a task using the create_task service.

    Returns:
        function: A callable that creates a task with specified parameters.

    """

    def _create_task(
        title="Default Title", description="Default Description", due_date="2025-01-01"
    ):
        return create_task(title, description, due_date)

    return _create_task


@pytest.fixture
def create_task_via_route(client):
    """Create a task by posting to the '/' route.

    Args:
        client (FlaskClient): The Flask test client.

    Returns:
        function: A callable that creates a task via the route.

    """

    def _create_task_via_route(
        title="Default Title", description="Default Description", due_date="2025-01-01"
    ):
        return client.post(
            "/",
            data={
                "title": title,
                "description": description,
                "due_date": due_date,
                "submit": True,
            },
            follow_redirects=True,
        )

    return _create_task_via_route
