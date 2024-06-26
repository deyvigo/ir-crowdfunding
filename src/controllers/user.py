from flask import request
from models import UserModel, MoneyModel, UserCategoryModel
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
    id_user_created = response[0]["last_row_id"]
    money = MoneyModel().create(id_user_created)
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
  
  @staticmethod
  @jwt_required()
  def get_user_by_username(username):
    response = UserModel().get_by_username(username)[0]["data"]

    id_user = response["id_user"]
    categories = UserCategoryModel().get_by_id_user(id_user)[0]["data"]
    response["categories"] = categories
    
    return response