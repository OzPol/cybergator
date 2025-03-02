from flask import Blueprint, jsonify, session
from app.services.sue_graph_service import get_sue_data

sue_bp = Blueprint("sue-graph", __name__)

@sue_bp.route("/", methods=["GET"])
def get_current_user():
    """Returns the stored SUE graph data."""
    if "user" not in session:
        return jsonify({"error": "User not logged in"}), 403
    return jsonify(get_sue_data())
