"""forms for user registration"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Optional


class AddUserForm(FlaskForm):
    """Forms for adding a user."""

    username = StringField("username:",
        validators= [InputRequired()])

    password = PasswordField("password:",
        validators= [InputRequired()])

    email = StringField("email",
        validators=[InputRequired()])

    first_name = StringField("first name:",
        validators= [InputRequired()])

    last_name = StringField("last name:",
        validators= [InputRequired()])



