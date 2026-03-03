from database import session as db_session, Login
from flask import render_template, request, redirect, url_for, session as flask_session, flash
from main import app
from werkzeug.security import check_password_hash, generate_password_hash

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = request.form.get("login_input")
        password_input = request.form.get("password_input")

        user = db_session.query(Login).filter_by(username=login_input).first()

        if user and check_password_hash(user.password, password_input):
            flask_session["user_id"] = login_input
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciais inválidas. Tente novamente.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")



@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", username=flask_session.get("user_id"))



@app.route("/logout")
def logout():
    flask_session.clear()
    return redirect(url_for("index"))