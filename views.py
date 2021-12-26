# <------------------------------------------------------------------------------------------------------------------> #
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from mainapp.models import UserLogin, Accounts, Users
from mainapp.settings import db

from mainapp.google_views import GoogleSheetsApp
from binance.client import Client
# <------------------------------------------------------------------------------------------------------------------> #
main = Blueprint('main', __name__)
# <------------------------------------------------------------------------------------------------------------------> #
def is_valid(req):
    if not len(req.form['title']) > 3: return False
    if not len(req.form['api_key']) > 5: return False
    if not len(req.form['secret_api_key']) > 5: return False
    if not len(req.form['email']) > 5: return False
    return True
# <------------------------------------------------------------------------------------------------------------------> #
@main.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Page not found')
# <------------------------------------------------------------------------------------------------------------------> #
@main.route('/')
@main.route('/login', methods=['POST', 'GET'])
def login():
    ''' Authorization '''
    if current_user.is_authenticated: return redirect(url_for('.index'))

    admin = Users.query.get(1)
    if request.method == 'POST':
        if request.form['username'] == admin.username and check_password_hash(generate_password_hash(request.form['password']), admin.password):
            userLogin = UserLogin().create(admin)
            login_user(userLogin)
            return redirect(url_for('.index'))
        else:
            flash('Invalid username / password')

    return render_template('login.html', title='Authorization | BinanceApp')
# <------------------------------------------------------------------------------------------------------------------> #
@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('.login'))
# <------------------------------------------------------------------------------------------------------------------> #
@main.route('/index', methods=['POST', 'GET'])
@login_required
def index():
    ''' Main page '''
    now = datetime.now()
    now = '{}.{}.{}'.format(now.day, now.month, now.year)

    if request.method == 'POST':
        if is_valid(request):
            try:
                Client(request.form['api_key'], request.form['secret_api_key']).get_account_status()

                account = Accounts(name=request.form['title'], api_key=request.form['api_key'], create_at=now,
                                   secret_api_key=request.form['secret_api_key'], email=request.form['email'])
                db.session.add(account)
                db.session.flush()
                db.session.commit()
                GoogleSheetsApp().create_new_account(request.form['title'])
                flash('Счет добавлен!', category='success')
            except Exception as e:
                print('Error: Step 59 {}'.format(e))
                flash('Эта учетная запись уже находится в системе / API или SECRET API введен неверно!', category='danger')
                db.session.rollback()
        else:
            flash('Заполните форму!', category='danger')

    return render_template('index.html', title='BinanceApp', menu=Accounts.query.order_by('id'))
# <------------------------------------------------------------------------------------------------------------------> #
@main.route('/close/<int:user_id>/')
def close_acc(user_id):
    ''' Close account on index '''

    try:
        account = Accounts.query.get(user_id)
        account.status = False
        GoogleSheetsApp().close_or_open_account(account.name, account.status)
        db.session.commit()
        flash(f'Счет: "{account.name}" был закрыт!', category='danger')
    except Exception as e:
        flash(f'Счет: "{account.name}" не был закрыт!', category='danger')
        print('Error: Step 82 {}'.format(e))
        db.session.rollback()

    return redirect(url_for('.index'))
# <------------------------------------------------------------------------------------------------------------------> #
@main.route('/open/<int:user_id>')
def open_acc(user_id):
    ''' Open account on index '''
    try:
        account = Accounts.query.get(user_id)
        account.status = True
        GoogleSheetsApp().close_or_open_account(account.name, account.status)
        db.session.commit()
        flash(f'Счет: "{account.name}" был открыт!', category='danger')
    except Exception as e:
        flash(f'Счет: "{account.name}" не был открыт!', category='danger')
        print('Error: Step 98 {}'.format(e))
        db.session.rollback()
# <------------------------------------------------------------------------------------------------------------------> #
@main.route('/show/<int:user_id>')
def show_user(user_id):
    account = Accounts.query.get(user_id)
    flash(f'''{account.api_key} {account.secret_api_key}''', category='window')
    return redirect(url_for('.index'))
# <------------------------------------------------------------------------------------------------------------------> #