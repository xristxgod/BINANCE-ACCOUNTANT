from flask import Blueprint, render_template, redirect, url_for, flash

from app.services.auth import is_auth


app = Blueprint('main', __name__)


@app.route('/')
@is_auth
def index():
    return render_template(
        'main/index.html'
    )
