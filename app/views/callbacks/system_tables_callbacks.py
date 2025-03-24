from dash import Input, Output, State, html, ctx, no_update
import dash
import requests
from app.views.pages.nodes_table import nodes_table_layout
from app.views.pages.cves_table import cves_table_layout
from app.views.pages.software_table import software_table_layout
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
    
    @app.callback(
        [Output("cves-table", "data"),
         Output("new-cve-id", "value"),
         Output("new-node-id", "value"),
         Output("error-message", "children")],
        [Input("add-cve-btn", "n_clicks"),
         Input("cves-table", "active_cell")],  # Handle both add & remove
        [State("new-cve-id", "value"),
         State("new-node-id", "value"),
         State("cves-table", "data"),
         State("cves-table", "derived_viewport_data")],
        prevent_initial_call=True
    )
    def modify_cve_table(n_clicks, active_cell, cve_id, node_id, cve_data, derived_viewport_data):
        """Handles adding and removing CVEs."""
        
        triggered_id = ctx.triggered_id
        nvd_score = ""

        if triggered_id == "add-cve-btn":
            # Adding a new CVE
            if not all([cve_id, node_id]):
                return cve_data, "", "", "❌ Missing required fields!"
            
            api_url = f"{API_BASE_URL}/{cve_id}"
            try:
                response = requests.get(api_url)
                if response.status_code != 200:
                    return cve_data, "", node_id, f"❌ No data found for CVE {cve_id}!"

                
                cve_data_response = response.json()
                nvd_score = cve_data_response.get("NVD Score", "N/A")
                cve_id = cve_data_response.get("CVE ID")

            except requests.exceptions.RequestException as e:
                return cve_data, "", "", f"❌ API Error fetching CVE: {str(e)}"

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
                return cve_data, cve_id, "", f"❌ No node found with ID {node_id}!"

            new_entry = {
                "CVE ID": cve_id,
                "NVD Score": nvd_score,
                "Node ID": node_id,
                "Node Name": node_name,
                "Remove": "❌"
            }
            cve_data.append(new_entry)

            save_nodes_data(nodes_data)  # Save to JSON
            return cve_data, "", "", ""

        elif triggered_id == "cves-table":
            # Removing a CVE
            if not active_cell or active_cell["column_id"] != "Remove":
                return no_update, no_update, no_update, no_update  # Ignore clicks outside "Remove" column

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

            # Remove from UI table correctly
            cve_data = [entry for entry in cve_data if entry["CVE ID"] != cve_to_remove]

            return cve_data, "", "", f"{cve_to_remove} removed from {node_id_to_remove}!"

        return no_update, no_update, no_update, no_update  
    

    # @app.callback(
    #     [Output("software-table", "data"),
    #     Output("new-software-id", "value"),
    #     Output("new-node-id", "value"),
    #     Output("error-message", "children")],
    #     [Input("add-software-btn", "n_clicks"),
    #     Input("software-table", "active_cell")],  # Handle both add & remove
    #     [State("new-software-id", "value"),
    #     State("new-node-id", "value"),
    #     State("new-software-make", "value"),
    #     State("new-software-description", "value"),
    #     State("new-software-category", "value"),
    #     State("new-rack-type", "value"),
    #     State("new-is-in-use", "value"),
    #     State("software-table", "data"),
    #     State("software-table", "derived_viewport_data")],
    #     prevent_initial_call=True
    # )

    # def modify_software_table(n_clicks, active_cell, software_id, node_id, software_make, 
    #                       software_description, category, rack_type, is_in_use, software_data, derived_viewport_data):
    #     """Handles adding and removing Software records in the table."""
        
    #     triggered_id = ctx.triggered_id

    #     # if triggered_id == "add-software-btn":
    #     #     # Validate required fields
    #     #     if not all([software_id, node_id, software_make, category]):
    #     #         return software_data, "", "", "❌ Missing required fields!"

    #     #     # Check if node exists
    #     #     nodes_data = get_nodes()
    #     #     node_name = None
    #     #     node_found = False

    #     #     for node in nodes_data:
    #     #         if node["node_id"] == node_id:
    #     #             node_name = node["node_name"]
    #     #             node_found = True

    #     #             if "Software" not in node:
    #     #                 node["Software"] = {}

    #     #             node["Software"][software_id] = {
    #     #                 "Software Make": software_make,
    #     #                 "Description": software_description or "N/A",
    #     #                 "Category": category,
    #     #                 "Rack Type": rack_type or "N/A",
    #     #                 "In Use": is_in_use or "false"
    #     #             }
    #     #             break
            
    #     #     if not node_found:
    #     #         return software_data, software_id, "", f"❌ No node found with ID {node_id}!"

    #     #     # Add software entry to table
    #     #     new_entry = {
    #     #         "Software ID": software_id,
    #     #         "Software Make": software_make,
    #     #         "Description": software_description or "N/A",
    #     #         "Category": category,
    #     #         "Rack Type": rack_type or "N/A",
    #     #         "In Use": is_in_use or "false",
    #     #         "Node ID": node_id,
    #     #         "Node Name": node_name,
    #     #         "Remove": "❌"
    #     #     }
    #     #     software_data.append(new_entry)

    #     #     save_nodes_data(nodes_data)  # Save updated data

    #     #     return software_data, "", "", ""

    #     # if triggered_id == "software-table":
    #     #     # Removing software entry
    #     #     if not active_cell or active_cell["column_id"] != "Remove":
    #     #         return no_update, no_update, no_update, no_update  # Ignore clicks outside "Remove" column

    #     #     row_idx = active_cell.get("row")
    #     #     selected_software = derived_viewport_data[row_idx]

    #     #     software_to_remove = selected_software["Software ID"]
    #     #     node_id_to_remove = selected_software["Node ID"]

    #     #     nodes_data = get_nodes()
    #     #     for node in nodes_data:
    #     #         if node["node_id"] == node_id_to_remove:
    #     #             if software_to_remove in node.get("Software", {}):
    #     #                 del node["Software"][software_to_remove]
    #     #             break

    #     #     save_nodes_data(nodes_data)

    #     #     # Remove from UI table
    #     #     software_data = [entry for entry in software_data if entry["Software ID"] != software_to_remove]

    #     #     return software_data, "", "", f"{software_to_remove} removed from {node_id_to_remove}!"

    #     # return no_update, no_update, no_update, no_update
        