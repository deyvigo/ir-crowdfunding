from flask import request
from models import UserModel
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

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
  
  @staticmethod
  @jwt_required()
  def update_profile():
    data = request.json

    if "biography" not in data or "paypal" not in data or "linkedin" not in data:
      return { "error": "no has ingresado los campos necesarios" }, 400
    
    user = get_jwt_identity()

    username = user["username"]
    
    biography = data["biography"]
    paypal = data["paypal"]
    linkedin = data["linkedin"]

    response = UserModel().update_rows(username, biography, paypal, linkedin)

    return response
