from flask import Blueprint, render_template

errors_bp = Blueprint("errors", __name__)


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    """Render a custom 404 error page.

    Args:
        error (Exception): The error that occurred.

    Returns:
        tuple: A tuple containing the rendered template and the HTTP status code.

    """
    return render_template("404.html"), 404
