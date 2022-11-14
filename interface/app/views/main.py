from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required


app = Blueprint('main', __name__)


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template(
        'main/login.html'
    )