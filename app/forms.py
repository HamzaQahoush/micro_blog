from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    remember_me = BooleanField('Remember me ')
    submit = SubmitField('sign in ')


class RegistrationForm(FlaskForm):
    username = StringField('username', [validators.InputRequired()])
    email = StringField('email', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])
    password2 = PasswordField('Repeat password ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('sign up ')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('please use a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('please use a different email')
