from flask import Blueprint

from controllers import MoneyController

money_blueprint = Blueprint("money", __name__)

@money_blueprint.route("/money/buy", methods=["PUT"])
def buy_money():
  return MoneyController.buy_money()