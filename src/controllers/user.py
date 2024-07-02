from flask import request
from models import UserModel, MoneyModel, UserCategoryModel, ProjectModel
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

bcrypt = Bcrypt()

class UserController:
  @staticmethod
  def register_user():
    data = request.json
    username = data["username"]
    password = data["password"]
    first_name = data["name"]
    last_name = data["lastName"]
    birthday = data["birthdate"]
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
  def update_profile_bio():
    data = request.json

    if "biography" not in data:
      return { "error": "no has ingresado los campos necesarios" }, 400
    
    user = get_jwt_identity()
    username = user["username"]
    biography = data["biography"]

    response = UserModel().update_bio(username, biography)
    return response
  
  @staticmethod
  @jwt_required()
  def update_profile_linkedin():
    data = request.json

    if "linkedin" not in data:
      return { "error": "no has ingresado los campos necesarios" }, 400
    
    user = get_jwt_identity()
    username = user["username"]
    linkedin = data["linkedin"]

    response = UserModel().update_linkedin(username, linkedin)
    return response
  
  @staticmethod
  @jwt_required()
  def get_user_by_username(username):
    response = UserModel().get_by_username(username)[0]["data"]

    id_user = response["id_user"]
    categories = UserCategoryModel().get_by_id_user(id_user)[0]["data"]
    response["categories"] = categories
    
    return response
  
  @staticmethod
  @jwt_required()
  def get_profile():
    user = get_jwt_identity()
    id_user = user["id_user"]

    response = UserModel().get_all_info_by_id(id_user)
    projects = ProjectModel().get_by_id_user(id_user)[0]["data"]

    data_response = response[0]["data"]
    data_response["projects"] = projects

    return response
  
  @staticmethod
  @jwt_required()
  def check_for_first_login():
    user = get_jwt_identity()
    id_user = user["id_user"]

    response = UserCategoryModel().get_by_id_user(id_user)

    # return [] if is firts login
    return response