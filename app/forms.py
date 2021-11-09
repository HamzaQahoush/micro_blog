from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    remember_me = BooleanField('Remember me ')
    submit = SubmitField('sign in ')


