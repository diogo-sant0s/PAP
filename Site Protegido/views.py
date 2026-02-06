from datetime import datetime
from database import session as db_session, Users
import re
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


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

    if user and password and check_password_hash(user.password, password):
        flask_session['user_id'] = user.id

        access_token = create_access_token(identity=user.id)
        print(access_token)


        return redirect(url_for('dash_page') + f'?token={access_token}')

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

        hashed_password = generate_password_hash(password)

        new_user = Users(
            email=email,
            password=hashed_password
        )
        db_session.add(new_user)
        db_session.commit()

        flask_session['user_id'] = new_user.id
        return redirect(url_for('dash_page') + '?registered=true')

    return render_template("login.html")


@app.route('/dashboard')
@jwt_required()
def dash_page():

    token = request.args.get("token")

    if not token:
        return "Token em falta", 401

    try:
        decoded = decode_token(token)

        print(decoded)  # debug

        user_id = decoded["sub"]   # 👈 AQUI

    except Exception as e:
        return f"Token inválido: {str(e)}", 401


    user_id = get_jwt_identity()
    return render_template("dashboard.html", user_id)

