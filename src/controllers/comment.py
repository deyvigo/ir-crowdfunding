from models import CommentModel, UserModel

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

class CommentController:
  @staticmethod
  @jwt_required()
  def post_comment():
    data = request.json

    if "id_project" not in data or "comment" not in data:
      return { "error": "no se han ingresado los datos necesarios" }, 400
    
    user = get_jwt_identity()

    id_user = user["id_user"]
    id_project = data["id_project"]
    comment = data["comment"]

    response = CommentModel().post_comment(id_user, id_project, comment)[0]

    if "error" in response:
      return response
    
    comment_response = CommentModel().get_by_id(response["last_row_id"])

    comment = comment_response[0]["data"]

    if comment:
      user = UserModel().get_by_id(comment["id_user"])
      comment["user"] = user[0]["data"]

    return comment