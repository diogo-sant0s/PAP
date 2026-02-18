from database import session as db_session, Login
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app
from sqlalchemy import text

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        login_input = request.form['login_input']
        password_input = request.form['password_input']

    query = f"SELECT * FROM user WHERE login = {login_input} AND password = {password_input}"
    result = db_session.execute(query).fetchone()

    if result:
        flask_session['user'] = login_input
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html", error="Credenciais inválidas.")
        

@app.route("/dashboard")
def dashboard():
    if "user_id" not in flask_session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


