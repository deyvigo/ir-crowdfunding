from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import ProjectModel, UserModel, CategoryModel

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

    data_project["creator"] = user
    data_project["category"] = category

    return { "data": data_project }, 200

