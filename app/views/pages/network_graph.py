from dash import html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from app.views.ui_text.system_graph_text import system_graph_description

def cytoscape_graph(graph_data):
    # Creates Cytoscape graph elements from JSON data
    elements = [
        {"data": {"id": node["data"]["id"], "label": node["data"]["label"]}} for node in graph_data["nodes"]
    ] + [
        {"data": {"source": edge["data"]["source"], "target": edge["data"]["target"]}} for edge in graph_data["edges"]
    ]
    return elements


def graph_layout():
    # Graph Layout Page
    return html.Div([
        html.H2("System Graph", className="text-center mb-4"),

        # Descriptive body copy
        system_graph_description(),    

        html.H5("Interactive System Graph", className="text-center mt-4 mb-2"),

        html.Button("Refresh Graph", id="refresh-graph-btn", n_clicks=1, className="btn btn-primary mb-3 d-block mx-auto"),

        # Graph with styled border
        html.Div(
            children=[
                cyto.Cytoscape(
                    id="system-graph",
                    layout={"name": "breadthfirst"},
                    style={"width": "100%", "height": "800px"},
                    elements=[],
                )
            ],
            style={
                "border": "3px solid #007BFF",
                "borderRadius": "10px",
                "padding": "10px",
                "marginTop": "10px",
                "marginBottom": "40px",
                "backgroundColor": "#f9f9f9"
            }
        ),
    ])
