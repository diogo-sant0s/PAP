from datetime import datetime
from database import session as db_session, User
import re
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in flask_session:
            return redirect(url_for('login_page') + '?error=Faça login para acessar.')
        return f(*args, **kwargs)
    return decorated_function


def is_strong_password(password):
    if len(password) < 8:
        return False

    has_upper = re.search(r'[A-Z]', password)
    has_digit = re.search(r'\d', password)
    has_symbol = re.search(r'[@$!%*?&]', password)

    return bool(has_upper and has_digit and has_symbol)

@app.route('/')
def home():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = db_session.query(User).filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            # Atualizar último login
            user.last_login = datetime.utcnow()
            db_session.commit()

            # Criar token JWT
            token = create_access_token(identity=user.id)

            # Sessão opcional (para páginas HTML)
            flask_session['user_id'] = user.id

            return redirect(url_for('dashboard') + f'?token={token}')

        return redirect(url_for('login_page') + '?error=Credenciais inválidas.')

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nome = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validar password
        if not is_strong_password(password):
            return redirect(url_for('register') + '?error=Senha fraca.')

        # Verificar email existente
        existing_user = db_session.query(User).filter_by(email=email).first()

        if existing_user:
            return redirect(url_for('register') + '?error=Email já em uso.')

        # Hash password
        hashed_password = generate_password_hash(password)

        new_user = User(
            nome=nome,
            email=email,
            password=hashed_password
        )

        db_session.add(new_user)
        db_session.commit()

        flask_session['user_id'] = new_user.id

        return redirect(url_for('dashboard') + '?registered=true')

    return render_template("register.html")



@app.route('/dashboard')
@jwt_required()
def dashboard():

    user_id = get_jwt_identity()

    user = db_session.query(User).filter_by(id=user_id).first()

    if not user:
        return redirect(url_for('login_page'))

    return render_template("dashboard.html", user=user)

@app.route('/logout')
def logout():
    flask_session.clear()
    return redirect(url_for('login_page') + '?logout=true')