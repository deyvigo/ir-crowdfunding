from flask import Blueprint
from controllers.genero import GeneroController

genero_blueprint = Blueprint("genero", __name__)

@genero_blueprint.route("/genero", methods=["POST"])
def registrar_genero():
  return GeneroController.registrar_genero()

@genero_blueprint.route("/genero", methods=["GET"])
def get_all_genero():
  return GeneroController.get_all_genero()