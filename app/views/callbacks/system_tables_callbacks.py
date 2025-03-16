from dash import Input, Output, State, html
import dash
from app.views.pages.nodes_table import nodes_table_layout
from app.views.pages.cves_table import cves_table_layout
from app.services.data_loader import get_nodes, save_nodes_data

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
        Output("new-nvd-score", "value"),
        Output("new-node-id", "value"),
        Output("new-node-name", "value")],
        Input("add-cve-btn", "n_clicks"),
        [State("new-cve-id", "value"),
        State("new-nvd-score", "value"),
        State("new-node-id", "value"),
        State("new-node-name", "value"),
        State("cves-table", "data")],
        prevent_initial_call=True
    )
    def add_new_cve(n_clicks, cve_id, nvd_score, node_id, node_name, existing_data):
        """Adds a new CVE entry dynamically."""
        # No update if any field is missing
        if not all([cve_id, nvd_score, node_id, node_name]):
            print("Missing input fields")  # Debugging
            return existing_data, "", "", "", ""

        # Append new CVE to the table
        new_entry = {
            "CVE ID": cve_id,
            "NVD Score": nvd_score,
            "Node ID": node_id,
            "Node Name": node_name,
            "Remove": "❌"
        }
        existing_data.append(new_entry)

        nodes_data = get_nodes()
        for node in nodes_data:
            if node["node_id"] == node_id:
                if "CVE" not in node:
                    node["CVE"] = []
                if "CVE_NVD" not in node:
                    node["CVE_NVD"] = {}

                node["CVE"].append(cve_id)
                node["CVE_NVD"][cve_id] = nvd_score

        save_nodes_data(nodes_data)
        return existing_data, "", "", "", ""  