from flask import Blueprint, jsonify
from app.services.data_loader import get_nodes

# Define a Blueprint for the Nodes routes
nodes_bp = Blueprint("nodes", __name__)

@nodes_bp.route("/", methods=["GET"])
def get_all_nodes():
    """Returns the full list of nodes from the JSON file."""
    try:
        nodes = get_nodes()
        return jsonify(nodes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
