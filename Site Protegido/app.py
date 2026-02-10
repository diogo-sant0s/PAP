from flask import Flask
from flask_session import Session
import os
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# JWT
app.config["JWT_SECRET_KEY"] = "pap-secret-key-2026"
jwt = JWTManager(app)

from views import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context='adhoc')
