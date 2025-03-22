from flask import Blueprint, jsonify
import os
import json
import networkx as nx
from app.services.resilience_score_calculator import (
    calculate_system_resilience,
    calculate_resilience_scores,
    calculate_and_save_individual_metrics,
    calculate_all_work_areas_risk_fuzzy,
    critical_function_weights
)

resilience_bp = Blueprint("resilience", __name__)

@resilience_bp.route("", methods=["GET"])
def get_resilience_score():
    # """ API endpoint to recalculate and return the system resilience score."""
    try:
        # Paths
        data_path = os.path.join(os.path.dirname(__file__), "../data/json/")
        nodes_file = os.path.join(data_path, "Nodes_Complete.json")
        risk_file = os.path.join(data_path, "Risk_Factors.json")
        fuzzy_file = os.path.join(data_path, "Fuzzy_Set.json")

        # Load inputs
        with open(nodes_file) as f:
            nodes_data = json.load(f)
        fuzzy_scores = calculate_all_work_areas_risk_fuzzy(risk_file, fuzzy_file)

        # Build graph
        G = nx.Graph()
        for node in nodes_data:
            G.add_node(node["node_id"])
            for neighbor in node.get("connected_to", []):
                G.add_edge(node["node_id"], neighbor)

        # Recalculate
        resilience_scores = calculate_resilience_scores(
            nodes_data, G, fuzzy_scores, critical_function_weights
        )
        system_score = calculate_system_resilience(resilience_scores)

        return jsonify({
            "system_resilience_score": system_score,
            "node_scores": resilience_scores
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
