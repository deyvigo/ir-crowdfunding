from flask import request
from models import CategoryModel

class CategoryController:
  @staticmethod
  def registrar_genero():
    data = request.json
    if "name" not in data:
      return { "error": "no has ingresado la categoría" }, 400
    
    all = CategoryModel().get_all()[0]["data"]
    all_categories = [cat["name"].lower() for cat in all]
    name = data["name"]

    if name.lower() in all_categories:
      return { "message": "la categoría ya existe" }, 409
    response = CategoryModel().crear(name)
    return response
  
  @staticmethod
  def get_all_genero():
    response = CategoryModel().get_all()
    return response