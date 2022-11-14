from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

import src.settings as settings
from ..forms import SignInForm
from ..services.auth import Admin


app = Blueprint('auth', __name__)


def _valid_admin(username: str, password: str) -> UserMixin:
    if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
        return Admin(username=username)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = SignInForm()
    if form.validate_on_submit():
        admin = _valid_admin(form.username.data, form.password.data)
        if admin:
            login_user(admin)
            return redirect(url_for('main.index'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template(
        'login.html',
        form=form
    )
