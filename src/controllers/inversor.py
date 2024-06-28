from flask import request
from models import InversorModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class InversorController:
  @staticmethod
  def registrar_inversor():
    data = request.json
    hashed_pass = bcrypt.generate_password_hash(data.get("password"))
    response = InversorModel().registrar_inversor(data.get("username"), hashed_pass, data.get("name"), data.get("last_name"), data.get("preferencia"), data.get("linkedin"))
    return response