from flask import Blueprint

from controllers import SearcherController

search_blueprint = Blueprint("searcher", __name__)

@search_blueprint.route("/search", methods=["POST"])
def search():
  return SearcherController.search_by_prefix()