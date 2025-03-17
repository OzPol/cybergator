from flask import Blueprint, jsonify
from app.services.cve_service import CVEService

# Define a Blueprint for the CVE routes
cve_bp = Blueprint("cve", __name__)

@cve_bp.route("/<cve_id>", methods=["GET"])
def get_cve_details(cve_id):
    """Controller to fetch CVE details and return as API response."""
    cve_info, status_code = CVEService.get_cve_info(cve_id)
    
    return jsonify(cve_info), status_code
