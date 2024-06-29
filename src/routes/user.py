from flask import Blueprint
from controllers import UserController

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/user/register", methods=["POST"])
def registrar_inversor():
  return UserController.register_user()