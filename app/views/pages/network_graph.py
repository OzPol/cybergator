
from dash import html, dcc
import dash_cytoscape as cyto

def cytoscape_graph(graph_data):
    # Creates Cytoscape graph elements from JSON data
    elements = [
        {"data": {"id": node["data"]["id"], "label": node["data"]["label"]}} for node in graph_data["nodes"]
    ] + [
        {"data": {"source": edge["data"]["source"], "target": edge["data"]["target"]}} for edge in graph_data["edges"]
    ]
    return elements  # Returns list of elements, not a full Cytoscape object


def graph_layout():
    # Graph Layout Page
    return html.Div([
        html.H3("System Graph", className="text-center"),
        html.Button("Refresh Graph", id="refresh-graph-btn", n_clicks=0, className="btn btn-primary"),
        dcc.Loading(
            id="loading-graph",
            type="circle",
            children=[
                cyto.Cytoscape(
                    id="system-graph",
                    layout={"name": "breadthfirst"},  # auto-layout: "cose" or "breadthfirst" 
                    style={"width": "100%", "height": "800px"}, #, "border": "1px solid black"},  # Debug border
                    elements=[],  # Initially empty, updated by callback
                )
            ],
        ),
    ])
