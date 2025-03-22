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
            style={"width": "100%", "height": "1200px"},
            zoom=1,
            minZoom=0.2,
            maxZoom=2,
            zoomingEnabled=True,
            userZoomingEnabled=True,
            panningEnabled=True,
            userPanningEnabled=True,
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "label": "data(label)",
                        "width": "40px",
                        "height": "40px",
                        "color": "#ffffff",
                        "font-size": "10px",
                        "text-valign": "center",
                        "text-halign": "center",
                        "border-width": 2,
                        "border-color": "#1B4F72",
                        "text-outline-color": "#1B4F72",
                        "text-outline-width": 1,
                    },
                },
                {
                    "selector": ".server",
                    "style": {
                        "background-color": "#FFA500",  # Orange
                        "shape": "triangle"
                    },
                },
                {
                    "selector": ".workstation",
                    "style": {
                        "background-color": "#2ECC71",  # Light green
                        "shape": "ellipse"
                    },
                },
                {
                    "selector": ".san",
                    "style": {
                        "background-color": "#DDA0DD",  # Plum / Violet
                        "shape": "round-rectangle"
                    },
                },
                {
                    "selector": ".san_archive",
                    "style": {
                        "background-color": "#9370DB",  # Medium Purple
                        "shape": "hexagon"
                    },
                },
                {
                    "selector": ".san_archive_backup",
                    "style": {
                        "background-color": "#708090",  # Slate Gray
                        "shape": "octagon"
                    },
                },
                {
                    "selector": ".switch",
                    "style": {
                        "background-color": "#ADD8E6",  # Light Blue
                        "shape": "rectangle"
                    },
                },
                {
                    "selector": ".router",
                    "style": {
                        "background-color": "#FFA07A",  # Light Orange
                        "shape": "diamond"
                    },
                },
                {
                    "selector": ".firewall",
                    "style": {
                        "background-color": "#FF6347",  # Tomato Red
                        "shape": "pentagon"
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#7f8c8d",
                        "width": 2,
                        "curve-style": "bezier",
                        "target-arrow-shape": "triangle",
                        "target-arrow-color": "#7f8c8d",
                        "arrow-scale": 1,
                    },
                },
            ]
        )
    ])
