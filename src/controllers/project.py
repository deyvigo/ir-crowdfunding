from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import ProjectModel, UserModel, CategoryModel, MoneyModel, UserProjectsModel, CommentModel

class ProjectController:
  @staticmethod
  @jwt_required()
  def create_project():
    data = request.json

    required_fields = ["goal", "title", "description", "instagram", "facebook", "phone", "id_category"]

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields: 
      return { "error": "no se han ingresado los datos necesarios" }, 400
    
    goal = data["goal"]
    title = data["title"]
    description = data["description"]
    instagram = data["instagram"]
    facebook = data["facebook"]
    phone = data["phone"]
    id_category = data["id_category"]
    
    user = get_jwt_identity()
    id_user = user["id_user"]

    response = ProjectModel().create(goal, title, description, instagram, facebook, phone, id_category, id_user)

    return response
  
  @staticmethod
  @jwt_required()
  def get_all_projects():
    response = ProjectModel().get_all()
    return response
  
  @staticmethod
  @jwt_required()
  def get_project_by_id(id_project):
    data_project = ProjectModel().get_by_id(id_project)[0]["data"]
    if not data_project:
      return { "error": "no se han encontrado resultados" }, 404
    
    id_user = data_project["id_user"]
    id_category = data_project["id_category"]

    user = UserModel().get_by_id(id_user)[0]["data"]
    category = CategoryModel().get_by_id(id_category)[0]["data"]
    is_liked = UserProjectsModel().is_liked(id_project, id_user)

    if is_liked:
      data_project["is_liked"] = True
    else:
      data_project["is_liked"] = False

    data_project["creator"] = user
    data_project["category"] = category

    # obtener comentarios
    comments = CommentModel().get_all_by_id_project(id_project)[0]["data"]

    for comment in comments:
      id_user = comment["id_user"]
      user = UserModel().get_by_id(id_user)[0]["data"]
      comment["user"] = user

    data_project["comments"] = comments

    return { "data": data_project }, 200
  
  @staticmethod
  @jwt_required()
  def contribute_project():
    data = request.json
    if "id_project" not in data or "amount" not in data:
      return { "error": "no se han ingresado los datos necesarios" }, 400
    
    id_project = data["id_project"]
    amount = int(data["amount"])
    user = get_jwt_identity()
    id_user = user["id_user"]

    project = ProjectModel().get_by_id(id_project)[0]["data"]

    if not project:
      return { "error": "no se ha encontrado el proyecto" }, 404
    
    # verificar que el usuario tenga suficiente dinero
    user_ondatabase = MoneyModel().get_by_id_user(id_user)[0]["data"]
    if user_ondatabase["quantity"] < amount:
      return { "error": "no tienes suficiente dinero" }, 400
    
    # contribuir al proyecto

    updated = ProjectModel().update_current_money(id_project, amount)

    if updated[0]["row_count"] == 0:
      return { "error": "no se ha podido actualizar el proyecto" }, 500
    
    # quitar dinero de la cuenta del usuario
    MoneyModel().update_quantity(id_user, -amount)
    
    project["current_money"] = project["current_money"] + amount

    return project, 200


