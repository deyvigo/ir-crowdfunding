from flask import Blueprint
from controllers import LoginController

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route("/login", methods=["POST"])
def login_inversor():
  return LoginController.login_user()