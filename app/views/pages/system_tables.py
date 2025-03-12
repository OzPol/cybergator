from dash import html, dcc
import dash_bootstrap_components as dbc

def system_tables_layout():
    """Render the System Tables Overview Page dynamically."""
    
    return html.Div([
        html.H3("System Tables", className="text-center mt-4"),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Nodes", className="card-title"),
                        html.P("List of system nodes and associated CVEs.", className="card-text"),
                        dbc.Button("View Table", id="nodes-table-btn", color="primary", n_clicks=0),
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "textAlign": "center"}
                ), width=6, className="mb-3"
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("CVEs", className="card-title"),
                        html.P("All CVEs found in the system with their NVD scores.", className="card-text"),
                        dbc.Button("View Table", id="cves-table-btn", color="primary", n_clicks=0),
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "textAlign": "center"}
                ), width=6, className="mb-3"
            ),
        ], className="justify-content-center"),

        # This holds which table we are viewing (like Graph Page)
        dcc.Store(id="selected-table", data=None),

        html.Div(id="table-content", style={"marginTop": "20px"}),  # Table will load here dynamically
    ],)
