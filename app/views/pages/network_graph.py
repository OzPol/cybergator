from dash import html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from app.views.ui_text.system_graph_text import system_graph_description

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
        html.H3("System Graph", className="text-center mb-4"),
        system_graph_description(),
        html.Button("Refresh Graph", id="refresh-graph-btn", n_clicks=1, className="btn btn-primary mb-3"),
        dbc.Row([
            # Left: Graph
            dbc.Col([
                html.Div([
                    cyto.Cytoscape(
                        id="system-graph",
                        layout={"name": "breadthfirst"}, # auto-layout: "cose" or "breadthfirst" 
                        style={"width": "100%", "height": "600px"},
                        elements=[], # Initially empty, updated by callback
                        minZoom=0.4,
                        maxZoom=1.3,
                        zoomingEnabled=True,
                    )
                ], style={
                    "border": "2px solid #007BFF",
                    "borderRadius": "10px",
                    "padding": "10px",
                    "marginTop": "10px",
                    "marginBottom": "40px",
                    "backgroundColor": "#f9f9f9"
                })
            ], width=9),

            # Right: Controls
            dbc.Col([
                html.H5("Graph Controls"),
                # html.Button("Refresh Graph", id="refresh-graph-btn", n_clicks=1, className="btn btn-primary mb-3"),

                dbc.Button("Add New Node", id="open-add-node-form", color="primary", className="mb-3"),

                dbc.Collapse([
                    dbc.Card([
                        dbc.CardHeader("New Node Details"),
                        dbc.CardBody([
                            dbc.Input(id="new-node-id", placeholder="Node ID", className="mb-2"),
                            dbc.Input(id="new-node-name", placeholder="Node Name", className="mb-2"),
                            dcc.Dropdown(id="node-type-selector", options=[], placeholder="Node Type", className="mb-2"),
                            dcc.Dropdown(id="critical-function-selector", options=[], multi=True, placeholder="Critical Functions", className="mb-2"),
                            dcc.Dropdown(id="connected-nodes-selector", options=[], multi=True, placeholder="Connect To", className="mb-2"),
                            dbc.Checkbox(id="critical-data-stored", label="Critical Data Stored?", className="mb-2"),
                            dcc.Dropdown(
                                id="backup-role",
                                options=[],  # will be populated dynamically using def update_backup_role_options(node_type):
                                value=None,  # Sets default selection
                                placeholder="Backup Role",
                                className="mb-2",
                                clearable=False
                            ),
                            dcc.Dropdown(id="data-redundancy", options=[{"label": "Yes", "value": "Yes"}, {"label": "No", "value": "No"}], placeholder="Data Redundancy", className="mb-2"),
                            dbc.Checkbox(id="redundancy", label="Redundancy Present?", className="mb-2"),
                            dcc.Dropdown(id="risk-factor", options=[
                                {"label": "Low", "value": "Low"},
                                {"label": "Medium", "value": "Medium"},
                                {"label": "High", "value": "High"}], placeholder="Risk", className="mb-2"),
                            dbc.Checkbox(id="switch-dependency", label="Depends on Switch?", className="mb-2"),
                            dbc.Label("Resilience Penalty (0.0 - 1.0)", className="mb-1"),
                            dbc.Input(id="resilience-penalty", placeholder="Resilience Penalty", type="number", value=0.1, className="mb-2"),
                            html.Hr(),
                            dbc.Checkbox(id="no-software-checkbox", label="No Software Installed", className="mb-2"),
                            dcc.Dropdown(id="software-make-selector", options=[], placeholder="Software Make", className="mb-2"),
                            dcc.Dropdown(id="software-version-selector", options=[], placeholder="Software Version", className="mb-2"),
                            dbc.Button("Create Node", id="submit-new-node", color="success", className="mt-3")
                        ])
                    ])
                ], id="add-node-form", is_open=False)
            ], width=3)
        ])
    ])
