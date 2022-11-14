from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user

import app.settings as settings
from ..services.auth import AdminMixin, AdminAuth, AdminStatus


app = Blueprint('auth', __name__)
auth = AdminAuth()


@app.route('/login', methods=['POST', 'GET'])
@login_required
def login():
    from ..forms import SignInForm
    form = SignInForm()
    if form.validate_on_submit():
        if form.is_valid():
            auth.admin_mixin = AdminMixin(username=form.username.data)
            if settings.ADMIN_2AF_CODE:
                auth.change_status(status=AdminStatus.AUTH_2FA)
                return redirect(url_for('auth.login_2fa'))
            login_user(auth.admin_mixin)
            return redirect(url_for('main.index'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template(
        'auth/login.html',
        form=form
    )


@app.route("/login/2fa", methods=['POST', 'GET'])
@login_required
def login_2fa():
    from ..forms import SignIn2FAForm
    form = SignIn2FAForm()
    if auth.status != 1:
        return redirect(url_for('auth.login'))
    if form.validate_on_submit():
        if form.code.data == auth.get_2fa_code():
            login_user(auth.admin_mixin)
            return redirect(url_for('main.index'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template(
        'auth/login_2fa.html',
        form=form
    )


@app.route('/logout')
def logout():
    pass