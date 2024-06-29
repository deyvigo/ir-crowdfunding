from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from models import UserProjectsModel

class UserProjectController:
  @staticmethod
  @jwt_required()
  def like_a_project():
    user = get_jwt_identity()
    id_user = user["id_user"]

    data = request.json

    if "id_project" not in data:
      return { "error": "no se han ingresado los datos necesarios" }, 400
    
    id_project = data["id_project"]

    check = UserProjectsModel().get_by_id_user_and_project(id_user, id_project)

    print(check)

    if check:
      return { "message": "ya le diste like a este post" }, 200

    response = UserProjectsModel().create(id_user, id_project)

    return response
  
  @staticmethod
  @jwt_required()
  def unlike_project():
    user = get_jwt_identity()
    id_user = user["id_user"]

    data = request.json
    if "id_project" not in data:
      return { "error": "no se han ingresado los datos necesarios" }, 400
    id_project = data["id_project"]

    response = UserProjectsModel().delete_by_id(id_user, id_project)
    return response