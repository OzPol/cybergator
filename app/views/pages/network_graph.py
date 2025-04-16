from dash import html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from app.views.ui_text.system_graph_text import system_graph_description
from app.views.pages.node_actions import render_node_controls
from app.views.pages.graph_controls import render_graph_controls

def cytoscape_graph(graph_data):
    # Creates Cytoscape graph elements from JSON data
    try: 
        elements = [
            {"data": {"id": node["data"]["id"], "label": node["data"]["label"]}} for node in graph_data["nodes"]
        ] + [
            {"data": {"source": edge["data"]["source"], "target": edge["data"]["target"]}} for edge in graph_data["edges"]
        ]
        return elements
    except Exception as e:
        print("ERROR IN cytoscape_graph():", e)
        return []

def graph_layout():
    # Graph Layout Page
    return html.Div([
        
        dcc.Store(id="show-node-form", data=False),
        
        html.H3("System Graph", className="text-center mb-4"),

        system_graph_description(),

        html.Button("Refresh Graph", id="refresh-graph-btn", n_clicks=1, className="btn btn-primary mb-3"),

        dbc.Row([
            # LEFT: Graph + buttons
            dbc.Col([
                html.Div([
                    cyto.Cytoscape(
                        id="system-graph",
                        layout={"name": "breadthfirst"},
                        style={"width": "100%", "height": "600px"},
                        elements=[],
                        minZoom=0.4,
                        maxZoom=1.3,
                        zoomingEnabled=True,
                    )
                ], style={
                    "border": "2px solid #007BFF",
                    "borderRadius": "10px",
                    "padding": "10px",
                    "marginTop": "10px",
                    "marginBottom": "20px",
                    "backgroundColor": "#f9f9f9"
                }),

                html.Div([
                    dbc.Button("Add Node", id="add-node-toggle", color="primary", className="me-2"),
                    dbc.Button("Remove Node", id="remove-node-button", color="primary", className="me-2"),
                    dbc.Button("Add Edge", id="add-edge-button", color="primary", className="me-2"),
                    dbc.Button("Remove Edge", id="remove-edge-button", color="primary")
                ], className="mt-3 d-flex justify-content-start flex-wrap")
            ], width=9),

            # RIGHT: Graph Controls tabs + form panel
            dbc.Col([
                html.H5("Graph Controls", className="text-center mb-2"),
                render_graph_controls(),
                html.Div(id="node-form-container", style={"marginTop": "20px"}),
                html.Div(id="create-node-feedback", style={"color": "green", "fontSize": "12px", "marginTop": "10px"}),
                html.Div(id="remove-node-feedback", style={"color": "red", "fontSize": "12px"})
            ], width=3)
        ])
    ])
    