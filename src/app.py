from flask import Flask, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from routes import category_blueprint, user_blueprint, login_blueprint, voice_blueprint, money_blueprint

app = Flask(__name__)

import os
UPLOAD_FOLDER = 'upload_audios'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)

CORS(app, origins=["http://localhost:5173", "http://localhost:5000"])

app.config["JWT_SECRET_KEY"] = "ir-crowdfunding"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.register_blueprint(category_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(voice_blueprint)
app.register_blueprint(money_blueprint)

@app.route("/helloworld", methods=["GET"])
def hello_world():
  return { "message": "Hello World" }

if __name__ == "__main__":
  app.run(debug=True)
