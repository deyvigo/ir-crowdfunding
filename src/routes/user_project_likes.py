from controllers import UserProjectController

from flask import Blueprint

user_project_blueprint = Blueprint("user_project", __name__)

@user_project_blueprint.route("/user/like/project", methods=["POST"])
def like_post():
  return UserProjectController.like_a_project()

@user_project_blueprint.route("/user/unlike/project", methods=["DELETE"])
def unlike_post():
  return UserProjectController.unlike_project()