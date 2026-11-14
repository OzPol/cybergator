from flask import Blueprint, jsonify
from app.services.sue_graph_service import get_sue_data

sue_bp = Blueprint("sue-graph", __name__)

@sue_bp.route("/", methods=["GET"])
def get_current_user():
    """Returns the stored SUE graph data."""
    return jsonify(get_sue_data())
