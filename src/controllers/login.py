from models.inversor import InversorModel
from flask import request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

class LoginController:
  @staticmethod
  def login_inversor():
    username = request.json.get("username")
    password = request.json.get("password")
    user_data = InversorModel().get_inversor_by_username(username)

    user = user_data.get("data")
    if (user):
      if (bcrypt.check_password_hash(user.get("password"), password)):
        acces_token = create_access_token(identity={
          "username": username,
          "id_inversor": user.get("id_inversor")
        })
        return { "token": acces_token }, 200
      else:
        return { "error": "Contraseña incorrecta" }, 401
    else:
      return { "error": "No existe el usuario" }, 404