# app/views/callbacks/neo4j_callbacks.py
from dash import Input, Output
import requests
from app.services.neo4j_graph_service import get_network_graph


def register_neo4j_callbacks(app):
    @app.callback(
        Output("neo4j-import-btn", "children"),
        Input("neo4j-import-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def trigger_neo4j_import(n_clicks):
        try:
            response = requests.post("http://localhost:8000/api/neo4j/import")
            if response.status_code == 200:
                return "✅ Imported! 😎🤙🏻🔥 "
            else:
                return "💔 Failed 👎"
        except Exception:
            return "⚠️🚩 Error"
        
    @app.callback(
        Output("cytoscape-neo4j", "elements"),
        Input("refresh-neo4j-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def refresh_graph(n_clicks):
        return get_network_graph()
