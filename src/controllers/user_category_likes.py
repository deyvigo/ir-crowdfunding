from flask import request

from models import UserCategoryModel, UserModel

class UserCategoryController:
  @staticmethod
  def add_category_to_user():
    data = request.json

    if "categories" not in data:
      return { "error": "no has ingresado los datos necesarios" }, 400
    
    categories = data["categories"]

    user_categories_pairs = []

    for category in categories:
      username = category["username"]
      id_category = category["id_category"]
      user = UserModel().get_by_username(username)[0]["data"]
      id_user = user["id_user"]
      user_categories_pairs.append((id_user, id_category))

    response = UserCategoryModel().create(user_categories_pairs)
    return response