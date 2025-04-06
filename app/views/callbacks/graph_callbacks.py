from dash import Input, Output, State
import requests
from app.views.pages.network_graph import cytoscape_graph
from dash.dependencies import Input, Output, State
from dash import ctx
import requests
from app.views.pages.network_graph import cytoscape_graph
from app.services.graph_service import add_node_to_system_graph
from app.services.data_loader import (
    get_software_dropdown_options, get_node_types, get_critical_functions,
    get_all_nodes, get_software_cves, append_software_entry, get_critical_function_keys
)

def register_graph_callbacks(app):
    @app.callback(
        Output("system-graph", "elements"),  
        Input("refresh-graph-btn", "n_clicks"),
        State("system-graph", "elements"),
    )
    def update_graph(n_clicks, current_elements):
        print(f"Callback triggered! n_clicks={n_clicks}")  # Debugging
        if n_clicks > 0:
            response = requests.get("http://127.0.0.1:8000/api/graph")  # API Call
            print(f"API Response Code: {response.status_code}")  # Debugging
            if response.status_code == 200:
                graph_data = response.json()
                print(f"Graph Data Received: {graph_data}")  # Debugging
                if "nodes" in graph_data and "edges" in graph_data:
                    updated_graph = cytoscape_graph(graph_data) # Update graph with API data
                    print(f"Graph Updated!")
                    return updated_graph
                return []  # Empty graph if no data
        return current_elements  # Keeps existing graph if no new data

    @app.callback(
        Output("collapse-system-info", "is_open"),
        Input("toggle-system-info", "n_clicks"),
        State("collapse-system-info", "is_open"),
    )
    def toggle_system_info(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open

    @app.callback(
        Output("add-node-form", "is_open"),
        Input("open-add-node-form", "n_clicks"),
        State("add-node-form", "is_open"),
        prevent_initial_call=True
    )
    def toggle_add_node_form(n_clicks, is_open):
        return not is_open
    
    @app.callback(
        Output("node-type-selector", "options"),
        Input("system-graph", "elements")
    )
    def populate_node_types(_):
        return [{"label": t, "value": t} for t in get_node_types()]
    
    @app.callback(
        Output("critical-function-selector", "options"),
        Input("system-graph", "elements")
    )
    def populate_critical_functions(_):
        return [{"label": fn, "value": fn} for fn in get_critical_function_keys()]


    @app.callback(
        Output("connected-nodes-selector", "options"),
        Input("system-graph", "elements")
    )
    def populate_connected_nodes(_):
        return get_all_nodes()

    @app.callback(
        Output("software-make-selector", "options"),
        Input("system-graph", "elements")
    )
    def populate_software_makes(_):
        make_options, _ = get_software_dropdown_options()
        return make_options
    
    @app.callback(
        Output("software-version-selector", "options"),
        Input("software-make-selector", "value"),
        prevent_initial_call=True
    )
    def update_versions_for_make(selected_make):
        _, software_dict = get_software_dropdown_options()
        return software_dict.get(selected_make, [])
