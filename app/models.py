from datetime import datetime
from typing import Optional

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()
migrate = Migrate()


class Task(db.Model):
    """Model representing a task."""

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[Optional[str]]
    due_date: Mapped[Optional[datetime]]
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        """Return a string representation of the Task object.

        Returns:
            str: A string representation of the Task object.

        """
        return f"<Task {self.title}>"
