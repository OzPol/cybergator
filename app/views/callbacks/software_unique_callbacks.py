from dash import html, Input, Output, State, ctx, no_update
import requests
from app.services.data_loader import get_software_cves

API_BASE_URL = "http://localhost:8000/api/software"

def register_software_unique_callbacks(app):
    """Register callbacks for unique software table actions."""

    @app.callback(
        [
            Output("software-unique-table", "data"),
            Output("expanded-software-details", "children"),
            Output("software-error-message", "children"),
            Output("add-new-software-make", "value"),
            Output("add-new-software-desc", "value"),
            Output("add-new-software-version", "value")
        ],
        [
            Input("add-software-btn", "n_clicks"),
            Input("software-unique-table", "active_cell")
        ],
        [
            State("add-new-software-make", "value"),
            State("add-new-software-desc", "value"),
            State("add-new-software-version", "value"),
            State("software-unique-table", "data"),
            State("software-unique-table", "derived_viewport_data")
        ],
        prevent_initial_call=True
    )
    def handle_add_or_table_click(n_clicks, active_cell, make, desc, version, table_data, viewport_data):
        triggered_id = ctx.triggered_id

        # Handle Add btn click
        if triggered_id == "add-software-btn":
            if not all([make, desc, version]):
                return no_update, no_update, "Missing required fields!", no_update, no_update, no_update

            payload = {
                "make": make,
                "description": desc,
                "version": version
            }

            try:
                response = requests.post(API_BASE_URL, json=payload)
                if response.status_code != 201:
                    return no_update, no_update, "❌ Failed to add software!", no_update, no_update, no_update

                new_id = response.json().get("id")
                new_entry = {
                    "Software ID": new_id,
                    "Make": make,
                    "Description": desc,
                    "Version": version,
                    "Expand": "➕",
                    "Remove": "❌"
                }

                table_data.append(new_entry)
                return table_data, "", "", "", "", ""

            except Exception as e:
                return no_update, no_update, f"API error: {str(e)}", no_update, no_update, no_update

        # Handle Remove or Expand from table clicks
        if not active_cell:
            return no_update, no_update, no_update, no_update, no_update, no_update

        row = active_cell["row"]
        column = active_cell["column_id"]
        software_id = table_data[row]["Software ID"]

        if column == "Remove":
            try:
                response = requests.delete(f"{API_BASE_URL}/{software_id}")
                if response.status_code != 200:
                    return no_update, no_update, "❌ Failed to remove software!", no_update, no_update, no_update

                updated_data = [entry for i, entry in enumerate(table_data) if i != row]
                return updated_data, "", "", no_update, no_update, no_update

            except Exception as e:
                return no_update, no_update, f"API error: {str(e)}", no_update, no_update, no_update

        elif column == "Expand":
            software_cves = get_software_cves().get(software_id, {})
            node_list = ", ".join(software_cves.get("nodes", [])) or "No assigned nodes"
            cve_list = ", ".join([f"{cve} (NVD: {score})" for cve, score in software_cves.get("cves", {}).items()]) or "No CVEs"

            details = html.Div([
                html.H5(f"Details for {software_id}"),
                html.P(f"Nodes: {node_list}"),
                html.P(f"CVEs: {cve_list}"),
            ])

            return no_update, details, "", no_update, no_update, no_update

        return no_update, no_update, no_update, no_update, no_update, no_update
