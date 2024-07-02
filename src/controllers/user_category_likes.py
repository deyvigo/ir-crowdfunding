from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import UserCategoryModel, UserModel

class UserCategoryController:
  @staticmethod
  @jwt_required()
  def add_category_to_user():
    data = request.json

    if "categories" not in data:
      return { "error": "no has ingresado los datos necesarios" }, 400
    
    categories = data["categories"]
    user_categories_pairs = []

    user = get_jwt_identity()
    id_user = user["id_user"]

    for category in categories:
      id_category = category["id_category"]
      user_categories_pairs.append((id_user, id_category))

    response = UserCategoryModel().create(user_categories_pairs)
    return response