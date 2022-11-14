from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired


class SignInForm(FlaskForm):
    username = StringField(label='Username:', validators=[Length(min=2, max=255), DataRequired()])
    password = PasswordField(label='Password:', validators=[Length(min=4, max=255), DataRequired()])
    submit = SubmitField(label='Sign in')

    def is_valid(self) -> bool:
        import app.settings as settings
        if self.username == settings.ADMIN_USERNAME and self.password == settings.ADMIN_PASSWORD:
            return True
        return False


class SignIn2FAForm(FlaskForm):
    code = IntegerField(label='Code:', validators=[Length(min=6, max=6), DataRequired()])
    submit = SubmitField(label='Sign in')

    def is_valid(self) -> bool:
        pass

