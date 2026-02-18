from database import session as db_session, Login
from flask import render_template, request, redirect, url_for, session as flask_session
from main import app
from sqlalchemy import text

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
    
        login_input = request.form.get("username")
        password_input = request.form.get("password")

    query = f"SELECT * FROM login WHERE username = '{login_input}' AND password = '{password_input}'"
    result = db_session.execute(text(query)).fetchone()

    if result:
        flask_session["user_id"] = login_input
        return redirect(url_for('main.dashboard'))
    
    else:
        return redirect(url_for("login"))



@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
