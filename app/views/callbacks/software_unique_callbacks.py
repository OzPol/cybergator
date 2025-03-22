from dash import html, Input, Output, State, ctx, no_update
import dash
import requests
from app.services.data_loader import get_software_cves, get_next_software_id, save_json

API_BASE_URL = "http://localhost:8000/api/software" 

def register_software_unique_callbacks(app):
    """Register callbacks for unique software table actions."""

    @app.callback(
        Output("expanded-software-details", "children"),
        Input("software-unique-table", "active_cell"),
        State("software-unique-table", "derived_viewport_data"),
        prevent_initial_call=True
    )
    def expand_software_details(active_cell, software_data):
        """Displays nodes & CVEs when expanding a software entry."""
        if not active_cell or active_cell["column_id"] != "Expand":
            return no_update

        row_idx = active_cell["row"]
        selected_software = software_data[row_idx]["Software ID"]
        software_cves = get_software_cves().get(selected_software, {})

        node_list = ", ".join(software_cves.get("nodes", [])) if software_cves.get("nodes") else "No assigned nodes"
        cve_list = ", ".join([f"{cve} (NVD: {score})" for cve, score in software_cves.get("cves", {}).items()]) if software_cves.get("cves") else "No CVEs"

        return html.Div([
            html.H5(f"Details for {selected_software}"),
            html.P(f"Nodes: {node_list}"),
            html.P(f"CVEs: {cve_list}"),
        ])

    @app.callback(
        [
            Output("software-unique-table", "data"),
            Output("error-message", "children"),
            Output("new-software-make", "value"),
            Output("new-software-desc", "value"),
            Output("new-software-version", "value")
        ],
        Input("add-software-btn", "n_clicks"),
        [
            State("new-software-make", "value"),
            State("new-software-desc", "value"),
            State("new-software-version", "value"),
            State("software-unique-table", "data")
        ],
        prevent_initial_call=True
    )
    def add_new_software(n_clicks, make, description, version, current_data):
        if not all([make, description, version]):
            return no_update, "Missing required fields!", no_update, no_update, no_update

        # 🔻 API call instead of local file manipulation
        payload = {
            "make": make,
            "description": description,
            "version": version
        }

        try:
            response = requests.post(API_BASE_URL, json=payload)
            if response.status_code != 201:
                return no_update, "❌ Failed to add software!", no_update, no_update, no_update
            
            new_id = response.json().get("id")  # Get generated ID from API response

            new_entry = {
                "Software ID": new_id,
                "Make": make,
                "Description": description,
                "Version": version,
                "Expand": "➕",
                "Remove": "❌"
            }
            current_data.append(new_entry)

            return current_data, "", "", "", ""

        except Exception as e:
            return no_update, f"API error: {str(e)}", no_update, no_update, no_update
