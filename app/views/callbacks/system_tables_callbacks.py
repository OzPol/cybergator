from dash import Input, Output, State, html, ctx, no_update
import dash
import requests
from app.views.pages.nodes_table import nodes_table_layout
from app.views.pages.cves_table import cves_table_layout
from app.services.data_loader import get_nodes, save_nodes_data

API_BASE_URL = "http://localhost:8000/api/cve"

def register_system_tables_callbacks(app):
    """Register callbacks to handle system table selection."""

    @app.callback(
        Output("selected-table", "data"),  # Stores which table is selected
        [Input("nodes-table-btn", "n_clicks"),
        Input("cves-table-btn", "n_clicks")],
        prevent_initial_call=True
    )
    def select_table(nodes_clicks, cves_clicks):
        """Updates selected table based on button clicked."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return triggered_id  # Stores selected table

    @app.callback(
        Output("table-content", "children"),
        Input("selected-table", "data")
    )
    def update_table_content(selected_table):
        """Loads table content dynamically."""
        print(f" Updating table content for: {selected_table}") 
        
        if selected_table == "nodes-table-btn":
            return html.Div([
                html.H4("Nodes Table"),
                html.P("This will show the full nodes table.")
            ])
        elif selected_table == "cves-table-btn":
            return html.Div([
                html.H4("CVEs Table"),
                html.P("This will show the full CVEs table.")
            ])
        return html.Div("Select a table to view its contents.")

    # Callback to add a new CVE entry
    @app.callback(
        [Output("cves-table", "data"),
        Output("new-cve-id", "value"),
        Output("new-node-id", "value"),
        Output("error-message", "children")],
        Input("add-cve-btn", "n_clicks"),
        [State("new-cve-id", "value"),
        State("new-node-id", "value"),
        State("cves-table", "data")],
        prevent_initial_call=True
    )
    def add_new_cve(n_clicks, cve_id, node_id, existing_data):
        """
            Adds a new CVE entry dynamically.
            CVE ids are validated and scores are pulled dynamically from the NVD database api. 
        """
        
        # No update if any field is missing
        if not all([cve_id, node_id]):
            return existing_data, "", "", "❌ Missing required fields!"
        
        # Fetch CVE details from Flask API
        api_url = f"{API_BASE_URL}/{cve_id}"
        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                return existing_data, "", node_id, f"❌ No data found for {cve_id}!"
            
            cve_data = response.json()
            nvd_score = cve_data.get("NVD Score", "N/A")
            cve_id = cve_data.get("CVE ID")

        except requests.exceptions.RequestException as e:
            return existing_data, "", "", f"❌ Error fetching CVE: {str(e)}"

        nodes_data = get_nodes()
        node_name = None
        node_found = False
        
        for node in nodes_data:
            if node["node_id"] == node_id:
                node_name = node["node_name"]
                node_found = True
                
                if "CVE" not in node:
                    node["CVE"] = []
                if "CVE_NVD" not in node:
                    node["CVE_NVD"] = {}

                node["CVE"].append(cve_id)
                node["CVE_NVD"][cve_id] = nvd_score
                break
           
        if not node_found:
            return existing_data, cve_id, "", f"❌ No node found with ID {node_id}!"
            
        # Append new CVE to the table
        new_entry = {
            "CVE ID": cve_id,
            "NVD Score": nvd_score,
            "Node ID": node_id,
            "Node Name": node_name,
            "Remove": "❌"
        }
        existing_data.append(new_entry)

        save_nodes_data(nodes_data)
        return existing_data, "", "", no_update