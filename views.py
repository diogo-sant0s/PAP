from datetime import datetime
from database import session as db_session, Acesso, Colaborador
from qr import generate_qr
import re
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in flask_session:
            return redirect(url_for('login') + '?error=Faça login para acessar.')
        return f(*args, **kwargs)
    return decorated_function

def is_strong_password(password):
    if len(password) < 8:
        return False
    has_upper = re.search(r'[A-Z]', password)
    has_digit = re.search(r'\d', password)
    has_symbol = re.search(r'[@$!%*?&]', password)
    return bool(has_upper or has_digit or has_symbol)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")

    email = request.form.get('email')
    password = request.form.get('password')

    user = db_session.query(Colaborador).filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        flask_session['user_id'] = user.id

        last = (
            db_session.query(Acesso)
            .filter_by(colaborador_id=user.id)
            .order_by(Acesso.id.desc())
            .first()
        )

        if not last or last.acao == "saida":
            acao = "entrada"
        else:
            acao = "saida"

        novo = Acesso(
            colaborador_id=user.id,
            acao=acao,
            data=datetime.utcnow()
        )

        db_session.add(novo)
        db_session.commit()

        return redirect(url_for('qr_page') + '?login=success&registo=' + acao)

    return redirect(url_for('login') + '?error=Credenciais inválidas')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('name')      
        email = request.form.get('email')    
        password = request.form.get('password')

        if not is_strong_password(password):
            return redirect(url_for('register') + '?error=Senha fraca. Use 8+ caracteres com maiúsculas, números ou símbolos.')

        existing_user = db_session.query(Colaborador).filter_by(email=email).first()
        if existing_user:
            return redirect(url_for('register') + '?error=Email já em uso.')

        hashed_password = generate_password_hash(password)

        new_user = Colaborador(
            nome=nome,
            email=email,
            password=hashed_password
        )
        db_session.add(new_user)
        db_session.commit()

        flask_session['user_id'] = new_user.id
        return redirect(url_for('qr_page') + '?registered=true')

    return render_template("register.html")

@app.route('/qr')
@login_required
def qr_page():
    user_id = flask_session.get('user_id')
    qr_base64, expires = generate_qr(user_id)
    return render_template("qr.html", qr_data=qr_base64, expires=expires)

@app.route('/scan')
@login_required
def scan():
    user_id = request.args.get("user")

    if not user_id:
        return "QR inválido", 400

    user = db_session.query(Colaborador).filter_by(id=user_id).first()

    if not user:
        return "Utilizador não encontrado", 404

    last = (
        db_session.query(Acesso)
        .filter_by(colaborador_id=user.id)
        .order_by(Acesso.id.desc())
        .first()
    )

    if not last or last.acao == "saida":
        acao = "entrada"
    else:
        acao = "saida"

    new_log = Acesso(
        colaborador_id=user.id,
        acao=acao,
        data=datetime.utcnow()
    )

    db_session.add(new_log)
    db_session.commit()

    return f"Registro efetuado: {acao}"



@app.route("/qr/<token>")
def qr_scan(token):
    colaborador = (
        db_session.query(Colaborador)
        .filter_by(qr_token=token)
        .first()
    )

    if not colaborador:
        return "QR inválido", 404

    acao = registrar_acesso(colaborador.id)

    return f"Acesso registado como: {acao}"
