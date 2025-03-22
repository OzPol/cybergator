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
            style={"width": "100%", "height": "700px", "backgroundColor": "#f7f7f7"},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "label": "data(label)",
                        "background-color": "#0074D9",
                        "color": "white",
                        "text-valign": "center",
                        "text-halign": "center",
                        "font-size": "14px",
                        "width": 40,
                        "height": 40,
                    }
                },
                {
                    "selector": "[node_type = 'Server']",
                    "style": {
                        "background-color": "#0074D9"  # Blue
                    }
                },
                {
                    "selector": "[node_type = 'Device']",
                    "style": {
                        "background-color": "#2ECC40"  # Green
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#B0BEC5",
                        "target-arrow-color": "#B0BEC5",
                        "target-arrow-shape": "triangle",
                        "curve-style": "bezier",
                        "width": 2,
                        "label": "data(label)",
                        "font-size": "10px",
                        "text-rotation": "autorotate",
                        "text-margin-y": -10,
                        "color": "#333"
                    }
                }
            ]
        )
    ])
