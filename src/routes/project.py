from flask import Blueprint

from controllers import ProjectController

project_blueprint = Blueprint("project", __name__)

@project_blueprint.route("/create/project", methods=["POST"])
def create_project():
  return ProjectController.create_project()

@project_blueprint.route("/get/all/projects", methods=["GET"])
def get_all_projects():
  return ProjectController.get_all_projects()

@project_blueprint.route("/get/project/id/<id_project>", methods=["GET"])
def get_project_by_id(id_project):
  return ProjectController.get_project_by_id(id_project)