from flask import Blueprint, jsonify
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "../data/json/Nodes_Complete.json")

graph_bp = Blueprint("graph", __name__)

@graph_bp.route("", methods=["GET"])  
def get_graph_data():
    """API endpoint to return nodes and their relationships"""
    try:
        # with open("app/data/json/Nodes_Complete.json", "r") as f:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)

        # Extract nodes
        nodes = [{"data": {"id": str(node["node_id"]), "label": node["node_name"]}} for node in data]

        # Extract edges dynamically from `connected_to`
        edges = []
        for node in data:
            if "connected_to" in node and isinstance(node["connected_to"], list):
                for target_id in node["connected_to"]:
                    edges.append({"data": {"source": str(node["node_id"]), "target": str(target_id)}})

        return jsonify({"nodes": nodes, "edges": edges}), 200
    
    except Exception as e:
        print(f" ERROR in get_graph_data: {e}") # Debugging
        return jsonify({"error": str(e)}), 500
