from dash import Input, Output, State, html, ctx, no_update
import dash
import requests
import subprocess
from app.views.pages.nodes_table import nodes_table_layout
from app.views.pages.cves_table import cves_table_layout
from app.views.pages.software_unique_table import software_unique_table_layout
from app.services.data_loader import (
    get_nodes, save_nodes_data,
    get_all_software, get_software_inventory
)



API_BASE_URL = "http://localhost:8000/api/cve"

def register_system_tables_callbacks(app):
    """Register callbacks to handle system table selection."""

    @app.callback(
        Output("selected-table", "data"),
        [
            Input("nodes-table-btn", "n_clicks"),
            Input("cves-table-btn", "n_clicks")
        ],
        prevent_initial_call=True
    )
    def select_table(nodes_clicks, cves_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return triggered_id

    @app.callback(
        Output("table-content", "children"),
        Input("selected-table", "data")
    )
    def update_table_content(selected_table):
        print(f"Updating table content for: {selected_table}")
        if selected_table == "nodes-table-btn":
            return nodes_table_layout()
        elif selected_table == "cves-table-btn":
            return cves_table_layout()
        elif selected_table == "software-unique-btn": 
            return software_unique_table_layout()
        return html.Div("Select a table to view its contents.")

    @app.callback(
        [
            Output("cves-table", "data"),
            Output("new-cve-id", "value"),
            Output("new-software-version", "value"),
            Output("error-message", "children")],
        [
            Input("add-cve-btn", "n_clicks"),
            Input("cves-table", "active_cell")],
        [
            State("new-cve-id", "value"),
            State("new-software-version", "value"),
            State("cves-table", "data"),
            State("cves-table", "derived_viewport_data")
        ],
        prevent_initial_call=True
    )
    def modify_cve_table(n_clicks, active_cell, cve_id, software_id, cve_data, derived_viewport_data):
        triggered_id = ctx.triggered_id

        if triggered_id == "add-cve-btn":
            if not all([cve_id, software_id]):
                return cve_data, "", "", "Missing CVE ID or Software selection!"

            # Fetch CVE details
            try:
                response = requests.get(f"{API_BASE_URL}/{cve_id}")
                if response.status_code != 200:
                    return cve_data, "", software_id, f"No data found for CVE {cve_id}!"
                cve_info = response.json()
                cve_id = cve_info.get("CVE ID")
                nvd_score = cve_info.get("NVD Score", "N/A")
            except Exception as e:
                return cve_data, "", "", f"API Error: {str(e)}"

            # Get affected nodes from CSV
            software_inventory = get_software_inventory()
            affected_node_ids = {entry["node_id"] for entry in software_inventory if entry["software_id"] == software_id}

            nodes_data = get_nodes()
            updates = 0

            for node in nodes_data:
                if node["node_id"] in affected_node_ids:
                    if "CVE" not in node:
                        node["CVE"] = []
                    if "CVE_NVD" not in node:
                        node["CVE_NVD"] = {}
                    if cve_id not in node["CVE"]:
                        node["CVE"].append(cve_id)
                        node["CVE_NVD"][cve_id] = nvd_score
                        cve_data.append({
                            "CVE ID": cve_id,
                            "NVD Score": nvd_score,
                            "Node ID": node["node_id"],
                            "Node Name": node["node_name"],
                            "Remove": "❌"
                        })
                        updates += 1

            if updates == 0:
                return cve_data, "", "", "⚠️ CVE already exists on all nodes."

            save_nodes_data(nodes_data)
            return cve_data, "", "", f"✅ CVE added to {updates} node(s)."

        elif triggered_id == "cves-table":
            if not active_cell or active_cell["column_id"] != "Remove":
                return no_update, no_update, no_update, no_update
            row_idx = active_cell.get("row")
            selected_cve = derived_viewport_data[row_idx]
            cve_to_remove = selected_cve["CVE ID"]
            node_id_to_remove = selected_cve["Node ID"]

            nodes_data = get_nodes()
            for node in nodes_data:
                if node["node_id"] == node_id_to_remove:
                    if cve_to_remove in node.get("CVE", []):
                        node["CVE"].remove(cve_to_remove)
                        node["CVE_NVD"].pop(cve_to_remove, None)
                    break

            save_nodes_data(nodes_data)
            
            # re-run the whole script
            subprocess.run(["python", "app/services/resilience_score_calculator.py"])
            
            cve_data = [entry for entry in cve_data if entry["CVE ID"] != cve_to_remove or entry["Node ID"] != node_id_to_remove]
            return cve_data, "", "", f"{cve_to_remove} removed from {node_id_to_remove}!"

        return no_update, no_update, no_update, no_update

    @app.callback(
        Output("new-software-version", "options"),
        Input("new-software-make", "value"),
        prevent_initial_call=True
    )
    def update_versions_for_selected_make(selected_make):
        if not selected_make:
            return []
        software_data = get_all_software()
        return software_data.get(selected_make, [])
