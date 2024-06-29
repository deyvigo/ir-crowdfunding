from flask import Blueprint
from controllers import UserController, UserCategoryController

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/user/register", methods=["POST"])
def register_user():
  return UserController.register_user()

@user_blueprint.route("/user/add/category", methods=["POST"])
def add_category_to_user():
  return UserCategoryController.add_category_to_user()