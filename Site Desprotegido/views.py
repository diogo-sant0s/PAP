from datetime import datetime
from database import session as db_session, Users
import re
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in flask_session:
            return redirect(url_for('login') + '?error=Faça login para acessar.')
        return f(*args, **kwargs)
    return decorated_function


def is_strong_password(password):
    if not password:
        return False
    if len(password) < 8:
        return False
    has_upper = re.search(r'[A-Z]', password)
    has_digit = re.search(r'\d', password)
    has_symbol = re.search(r'[@$!%*?&]', password)
    return bool(has_upper and has_digit and has_symbol)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form.get('email', '').lower().strip()
    password = request.form.get('password')

    user = db_session.query(Users).filter_by(email=email).first()

    if user and password and user.password == password:
        flask_session['user_id'] = user.id


        return redirect(url_for('dash_page') + '?login=success&registo=')

    return redirect(url_for('login') + '?error=Credenciais inválidas')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').lower().strip()
        password = request.form.get('password')

        print("PASSWORD RECEBIDA:", repr(password))

        if not is_strong_password(password):
            return redirect(url_for('register') + '?error=Senha fraca. Use 8+ caracteres com maiúsculas, números ou símbolos.')

        existing_user = db_session.query(Users).filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('register') + '?error=Email já em uso.')


        new_user = Users(
            email=email,
            password=password,
        )
        db_session.add(new_user)
        db_session.commit()

        flask_session['user_id'] = new_user.id
        return redirect(url_for('dash_page') + '?registered=true')

    return render_template("login.html")


@app.route('/dashboard')
@login_required
def dash_page():
    user_id = flask_session.get('user_id')
    return render_template("dashboard.html")

