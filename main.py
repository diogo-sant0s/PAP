from flask import Flask
from flask_session import Session
app = Flask(__name__)
app.secret_key = 'pap'  
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

from views import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)