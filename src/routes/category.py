from flask import Blueprint
from controllers import CategoryController

category_blueprint = Blueprint("category", __name__)

@category_blueprint.route("/create/category", methods=["POST"])
def registrar_genero():
  return CategoryController.registrar_genero()

@category_blueprint.route("/get/all/category", methods=["GET"])
def get_all_genero():
  return CategoryController.get_all_genero()