from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

import app.settings as settings
from ..services.auth import Admin


class AdminAuth:
    pass


app = Blueprint('auth', __name__)


@app.route('/login', methods=['POST', 'GET'])
def login():
    from ..forms import SignInForm
    form = SignInForm()
    if form.validate_on_submit():
        if form.is_valid():
            admin = Admin(username=form.username.data)
            if settings.ADMIN_2AF:
                return redirect(url_for('auth.login_2fa'))
            login_user(admin)
            return redirect(url_for('auth.login_2fa'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template(
        'auth/login.html',
        form=form
    )


@app.route("/login/2fa/<username>", methods=['POST', 'GET'])
def login_2fa(username: str):
    from ..forms import SignIn2FAForm
    form = SignIn2FAForm()
    return render_template(
        'auth/login_2fa.html',
        form=form
    )


@app.route('/logout')
def logout():
    pass