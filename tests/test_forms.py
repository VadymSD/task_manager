from app.forms import TaskForm


def test_valid_form(client):
    """Test form validation with correct data.

    Args:
        client (FlaskClient): The Flask test client.

    Returns:
        None

    """
    form = TaskForm(
        title="Valid Task", description="A valid description", due_date="2030-01-01"
    )
    assert form.validate()


def test_invalid_form_empty_title(client):
    """Test that a missing title fails validation.

    Args:
        client (FlaskClient): The Flask test client.

    Returns:
        None

    """
    form = TaskForm(title="", description="A description", due_date="2030-01-01")
    assert not form.validate()
    assert "This field is required." in form.title.errors
