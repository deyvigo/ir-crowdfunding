from flask import Flask, request, send_from_directory, send_file
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
from routes import category_blueprint, user_blueprint, login_blueprint, voice_blueprint, money_blueprint, project_blueprint, user_project_blueprint, search_blueprint, comment_blueprint

app = Flask(__name__)

import os
UPLOAD_FOLDER = 'upload_audios'
IMG_PROJECTS_FOLDER = 'upload_image_projects'
if not os.path.exists(UPLOAD_FOLDER):
  os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(IMG_PROJECTS_FOLDER):
  os.makedirs(IMG_PROJECTS_FOLDER)

CORS(app, origins=["http://localhost:5173", "http://localhost:5000"])

app.config["JWT_SECRET_KEY"] = "ir-crowdfunding"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMG_PROJECTS_FOLDER'] = IMG_PROJECTS_FOLDER

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.register_blueprint(category_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(voice_blueprint)
app.register_blueprint(money_blueprint)
app.register_blueprint(project_blueprint)
app.register_blueprint(user_project_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(comment_blueprint)

@app.route("/helloworld", methods=["GET"])
def hello_world():
  return { "message": "Hello World" }

@app.route("/img/project/<filename>", methods=["GET"])
def get_img_project(filename):
  print(filename)
  # retroceder un directorio
  path_file = os.path.join(os.path.dirname(__file__), "..", IMG_PROJECTS_FOLDER, filename)
  return send_file(path_file)

if __name__ == "__main__":
  app.run(debug=True)
