from flask import request
from models import UserModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserController:
  @staticmethod
  def register_user():
    data = request.json
    username = data["username"]
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    birthday = data["birthday"]
    user = UserModel().get_by_username(username)[0]["data"]
    if user:
      return { "error": "el usuario ya existe" }, 409
    hashed_pass = bcrypt.generate_password_hash(password)
    response = UserModel().register(username, hashed_pass, first_name, last_name, birthday)
    return response
