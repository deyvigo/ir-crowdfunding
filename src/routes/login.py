from flask import Blueprint
from controllers.login import LoginController

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route("/login/inversor", methods=["POST"])
def login_inversor():
  return LoginController.login_inversor()