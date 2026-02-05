from flask import Flask
from flask_session import Session
from flask_jwt_extended import JWTManager
from views import *

app = Flask(__name__)
app.secret_key = 'pap'  
app.config['SESSION_TYPE'] = 'filesystem'

# jwt
app.config["JWT_SECRET_KEY"] = "Super-hyper-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 #1 Hora e expira
jwt =JWTManager(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

Session(app)