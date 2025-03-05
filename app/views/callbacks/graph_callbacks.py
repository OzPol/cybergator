from dash import Input, Output, State
import requests
from app.views.pages.network_graph import cytoscape_graph

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
