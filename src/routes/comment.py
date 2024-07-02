from flask import Blueprint

from controllers import CommentController

comment_blueprint = Blueprint("comment", __name__)

@comment_blueprint.route("/create/comment", methods=["POST"])
def create_comment():
  return CommentController.post_comment()