from flask import Blueprint, jsonify
from app.databases.neo4j_db import Neo4jUnavailable
from app.services.neo4j_importer import create_nodes_and_relationships

neo4j_bp = Blueprint("neo4j", __name__)


@neo4j_bp.post("/import")
def import_graph():
    try:
        create_nodes_and_relationships()
    except Neo4jUnavailable as error:
        return jsonify({"error": str(error)}), 503
    except Exception:
        return jsonify({"error": "Neo4j import failed."}), 503
    return jsonify({"message": "Graph imported successfully."}), 200
