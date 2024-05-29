from flask import request
from models.genero import GeneroModel

class GeneroController:
  @staticmethod
  def registrar_genero():
    data = request.json
    response = GeneroModel().registrar_genero(data.get('nombre_genero'))
    return response
  
  @staticmethod
  def get_all_genero():
    response = GeneroModel().get_all_generos()
    return response