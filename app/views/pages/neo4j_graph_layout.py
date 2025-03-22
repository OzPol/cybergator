from dash import html
import dash_cytoscape as cyto
from app.services.neo4j_graph_service import get_network_graph

def neo4j_graph_layout():
    return html.Div([
        html.H3("Neo4j System Graph", style={"textAlign": "center", "color": "#333"}),

        cyto.Cytoscape(
            id="cytoscape-neo4j",
            elements=get_network_graph(),
            layout={"name": "cose"},
            style={"width": "100%", "height": "700px"},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "label": "data(label)",
                        "background-color": "#888",
                        "color": "white",
                        "text-valign": "center",
                        "text-halign": "center",
                        "font-size": "12px",
                        "width": "40px",
                        "height": "40px",
                        "border-color": "#000",
                        "border-width": 2,
                    }
                },
                {
                    "selector": "[node_type = 'Server']",
                    "style": {
                        "background-color": "#0074D9"  # Blue for servers
                    }
                },
                {
                    "selector": "[node_type = 'Device']",
                    "style": {
                        "background-color": "#2ECC40"  # Green for devices
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#999",
                        "target-arrow-color": "#999",
                        "target-arrow-shape": "triangle",
                        "curve-style": "bezier",
                        "width": 2,
                        "label": "data(label)",
                        "font-size": "10px",
                        "color": "#222"
                    }
                }
            ]
        )
    ])
