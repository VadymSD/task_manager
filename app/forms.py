from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, Length, Optional


class TaskForm(FlaskForm):
    """Form for creating a new task."""

    title = StringField("Title", validators=[DataRequired(), Length(max=100)])
    description = StringField(
        "Description", validators=[DataRequired(), Length(max=300)]
    )
    due_date = DateField("Due date", validators=[Optional()])
    submit = SubmitField("Create Task")
