from flask import Blueprint, jsonify
from app.services.neo4j_importer import create_nodes_and_relationships  # Make sure this is moved to services

neo4j_bp = Blueprint("neo4j", __name__)

@neo4j_bp.route("/import", methods=["POST"])
def import_to_neo4j():
    try:
        create_nodes_and_relationships()
        return jsonify({"message": "✅ Neo4j graph populated with nodes and relationships"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
