from flask import Blueprint
from controllers import UserController, UserCategoryController

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/user/register", methods=["POST"])
def register_user():
  return UserController.register_user()

@user_blueprint.route("/user/add/category", methods=["POST"])
def add_category_to_user():
  return UserCategoryController.add_category_to_user()

@user_blueprint.route("/user/update/profile/bio", methods=["PUT"])
def update_profile():
  return UserController.update_profile_bio()

@user_blueprint.route("/user/update/profile/linkedin", methods=["PUT"])
def update_linkedin():
  return UserController.update_profile_linkedin()

@user_blueprint.route("/user/update/profile/image", methods=["PUT"])
def update_profile_image():
  return UserController.update_profile_image()

# check if is first login
@user_blueprint.route("/user/first/login", methods=["GET"])
def get_simple_profile_info():
  return UserController.check_for_first_login()

@user_blueprint.route("/user/get/profile", methods=["GET"])
def get_profile_info():
  return UserController.get_profile()

@user_blueprint.route("/get/user/username/<username>", methods=["GET"])
def get_user_by_username(username):
  return UserController.get_user_by_username(username)