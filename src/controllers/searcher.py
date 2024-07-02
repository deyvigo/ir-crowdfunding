from utils.structure.Trie import Trie
from flask import request
from flask_jwt_extended import jwt_required

from models import ProjectModel

class SearcherController:
  @staticmethod
  @jwt_required()
  def search_by_prefix():
    data = request.json
    if "id_category" not in data or "prefix" not in data:
      return { "error": "no has ingresado los campos necesarios" }, 400
    
    id_category = data["id_category"]
    prefix = data["prefix"]

    all_projects_by_category = ProjectModel().get_by_id_category(id_category)[0]["data"]
    trie = Trie()

    map_projects = {}
    for project in all_projects_by_category:
      key = project["title"].lower()
      map_projects[key] = project
      trie.insert(project["title"].lower())

    results = trie.search(prefix.lower())
    response = []
    for result in results:
      response.append(map_projects[result])

    return response