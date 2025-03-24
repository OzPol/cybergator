from flask import Blueprint, jsonify, request
from app.services.data_loader import get_software_cves, save_json, get_next_software_id

software_bp = Blueprint("software", __name__)

@software_bp.route("/", methods=["GET"])
def get_all_software_cves():
    """Return full software_cves.json content."""
    return jsonify(get_software_cves()), 200

@software_bp.route("/", methods=["POST"])
def add_software_entry():
    """Add new software to software_cves.json."""
    data = request.get_json()

    required_fields = ["make", "description", "version"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    software_data = get_software_cves()
    new_id = get_next_software_id()

    software_data[new_id] = {
        "make": data["make"],
        "description": data["description"],
        "version": data["version"],
        "cves": {},
        "nodes": []
    }

    save_json(software_data, "software_cves.json")
    return jsonify({"message": "Software added", "id": new_id}), 201
