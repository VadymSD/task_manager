def test_not_found_error(client):
    """Test the custom 404 error page.

    Args:
        client (FlaskClient): The Flask test client.

    Returns:
        None

    """
    response = client.get("/random_page")
    assert response.status_code == 404
    assert b"<h1>Page not found</h1>" in response.data
