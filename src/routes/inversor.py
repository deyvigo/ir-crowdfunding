from flask import Blueprint
from controllers.inversor import InversorController

inversor_blueprint = Blueprint("inversor", __name__)

@inversor_blueprint.route("/inversor", methods=["POST"])
def registrar_inversor():
  return InversorController.registrar_inversor()