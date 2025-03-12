from flask import Blueprint, jsonify
import os
import json

# Define Blueprint
system_tables_bp = Blueprint("system_tables", __name__)

# Path to the JSON data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "../data/json/Nodes_Complete.json")

def load_nodes_data():
    """Load nodes from JSON file and extract required details."""
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)

        nodes_summary = []
        cves_summary = {}

        for node in data:
            # Collect Node Table Data
            total_cves = len(node["CVE"])
            max_nvd_score = max(node["CVE_NVD"].values(), default=0)  # Get highest CVE score
            
            nodes_summary.append({
                "node_id": node["node_id"],
                "node_name": node["node_name"],
                "node_type": node["node_type"],
                "risk_factor": node["risk_factor"],
                "total_cves": total_cves,
                "max_nvd_score": max_nvd_score
            })

            # Collect CVEs Summary
            for cve, score in node["CVE_NVD"].items():
                if cve not in cves_summary:
                    cves_summary[cve] = {"nvd_score": score, "nodes_affected": set()}
                cves_summary[cve]["nodes_affected"].add(node["node_name"])

        # Convert node sets to lists for JSON serialization
        for cve in cves_summary:
            cves_summary[cve]["nodes_affected"] = list(cves_summary[cve]["nodes_affected"])

        return {
            "nodes": nodes_summary,
            "cves": [{"cve_id": cve, "nvd_score": data["nvd_score"], "nodes_affected": data["nodes_affected"]} for cve, data in cves_summary.items()]
        }
    except Exception as e:
        return {"error": str(e)}

# API Endpoint to get system tables data
@system_tables_bp.route("", methods=["GET"])
def get_system_tables():
    """Returns available system tables overview."""
    try:
        data = load_nodes_data()

        if "error" in data:
            return jsonify({"error": data["error"]}), 500

        tables_metadata = {
            "nodes": {
                "title": "Nodes",
                "description": "List of system nodes and associated CVEs.",
                "count": len(data["nodes"])
            },
            "cves": {
                "title": "CVEs",
                "description": "All CVEs found in the system with their NVD scores.",
                "count": len(data["cves"])
            }
        }

        return jsonify({"tables": tables_metadata}), 200
    except Exception as e:
        print(f"ERROR in get_system_tables: {e}")
        return jsonify({"error": str(e)}), 500
