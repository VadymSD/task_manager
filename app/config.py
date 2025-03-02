import logging
import os


class Config:
    """Base configuration."""

    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    @staticmethod
    def init_app(app):
        """Initialize logging with minimal configuration."""
        logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL, logging.INFO))
        app.logger.setLevel(getattr(logging, Config.LOG_LEVEL, logging.INFO))
        app.logger.info("Logging has been configured!")
