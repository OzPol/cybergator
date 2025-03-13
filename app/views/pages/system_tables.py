from dash import html, dcc
import dash_bootstrap_components as dbc

def system_tables_layout():
    """Render the System Tables Overview Page dynamically."""
    
    return dbc.Container([
        html.H3("System Tables", className="text-center mt-4"),

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Nodes", className="card-title"),
                        html.P("List of system nodes and associated CVEs.", className="card-text"),
                        dbc.Button("View Table", href="/system-tables/nodes", color="primary"),  
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
                        dbc.Button("View Table", href="/system-tables/cves", color="primary"),  
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "textAlign": "center"}
                ), width=6, className="mb-3"
            ),
        ], className="justify-content-center"),
    ], fluid=True) 
# 