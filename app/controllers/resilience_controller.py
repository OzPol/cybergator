from flask import Blueprint, jsonify
from app.services.resilience_score_calculator import (
    calculate_system_resilience,
    calculate_resilience_scores,
    resilience_scores  # Directly use the precomputed scores
)

resilience_bp = Blueprint("resilience", __name__)

@resilience_bp.route("", methods=["GET"])
def get_resilience_score():
    """API endpoint to return the system resilience score."""
    try:
        # Use the resilience scores that were already calculated
        system_resilience = calculate_system_resilience(resilience_scores)

        return jsonify({
            "system_resilience_score": system_resilience,
            "node_scores": resilience_scores
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
