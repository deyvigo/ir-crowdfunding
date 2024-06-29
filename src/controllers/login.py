from models import UserModel
from flask import request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

class LoginController:
  @staticmethod
  def login_user():
    username = request.json.get("username")
    password = request.json.get("password")
    user_data = UserModel().get_by_username(username)[0]

    user = user_data["data"]
    if (user):
      if (bcrypt.check_password_hash(user.get("password"), password)):
        acces_token = create_access_token(identity={
          "username": username,
          "user": user["id_user"]
        })
        return { "token": acces_token }, 200
      else:
        return { "error": "Contraseña incorrecta" }, 401
    else:
      return { "error": "No existe el usuario" }, 404