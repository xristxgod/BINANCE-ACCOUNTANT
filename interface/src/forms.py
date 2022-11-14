from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, Length, DataRequired


class SignInForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=255), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=4, max=255), DataRequired()])
    submit = SubmitField(label='Sign in')
