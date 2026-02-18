from database import session as db_session, Login
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    login_input = request.form.get("login_input", "").strip().lower()
    password_input = request.form.get("password_input", "")

    # Login seguro usando ORM (evita SQL Injection)
    user = db_session.query(Login).filter_by(username=login_input).first()

    if user and password_input and user.password == password_input:
        flask_session["user_id"] = user.id
        return redirect(url_for("dashboard"))

    return render_template("login.html", error="Credenciais inválidas.")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in flask_session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    flask_session.clear()
    return redirect(url_for("login"))

