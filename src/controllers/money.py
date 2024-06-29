from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import MoneyModel

class MoneyController:
  @staticmethod
  @jwt_required()
  def buy_money():
    data = request.json

    if "quantity" not in data:
      return { "error": "no se han ingresado los campos necesarios" }, 400

    user = get_jwt_identity()

    id_user = user["id_user"]

    money_regist = MoneyModel().get_by_id_user(id_user)[0]["data"]
    print(money_regist)
    old_quantity = money_regist["quantity"]
    quantity_to_add = data["quantity"]

    quantity = int(quantity_to_add) + int(old_quantity)

    response = MoneyModel().update_quantity(id_user, quantity)

    return response