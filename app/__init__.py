from flask import Flask

from app.config import Config
from app.models import db, migrate


def create_app(config_object=None):
    """Create and configure the Flask application.

    Args:
        config_object (str): The configuration object to use.

    Returns:
        Flask: The configured Flask application.

    """
    app = Flask(__name__)

    app.config.from_object(Config)
    if config_object:
        app.config.update(config_object)
    Config.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.blueprints.errors.errors import errors_bp
    from app.blueprints.main.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    return app
