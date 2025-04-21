from dash import html, dcc
import dash_bootstrap_components as dbc

def system_tables_layout():
    """Render the System Tables Overview Page dynamically."""
    
    return dbc.Container([
        html.H2("System Tables", className="text-center mt-4"),

        # New Introductory Text Block
        dbc.Row(
            dbc.Col([
                html.P("System Tables store and organize essential data related to the system’s cyber resilience.", className="mb-3"),
                html.P("Users can view, add, update, and remove entries, ensuring system configurations are accurately reflected for analysis.", className="mb-4"),
            ], width=8, className="text-center"),  # narrower width + centered text
            justify="center"
        ), 

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

        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Software Nodes", className="card-title"),
                        html.P("List of software nodes and their details.", className="card-text"),
                        dbc.Button("View Table", href="/system-tables/software-nodes", color="primary"),  
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "textAlign": "center"}
                ), width=6, className="mb-3"
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Critical Functions", className="card-title"),
                        html.P("List of Critical Functions.", className="card-text"),
                        dbc.Button("View Table", href="/system-tables/critical-functions", color="primary"),  
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "textAlign": "center"}
                ), width=6, className="mb-3"
            ),
        ], className="justify-content-center"),
        
        # Unique Software Table (Not with Nodes)
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Unique Software", className="card-title"),
                        html.P("View and manage all unique software entries.", className="card-text"),
                        dbc.Button("View Table", href="/system-tables/software-unique", color="primary"),
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "textAlign": "center"}
                ), width=6, className="mb-3"
            ),
            # PLACE HOLDER FOR FUTURE TABLE Management
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H5("Coming Soon", className="card-title"),
                        html.P("Reserved for future software management tools.", className="card-text"),
                        dbc.Button("View Table", href="#", color="secondary", disabled=True),
                    ]),
                    className="shadow-sm p-3 mb-4 bg-white rounded",
                    style={"width": "100%", "textAlign": "center"}
                ), width=6, className="mb-3"
            ),
        ], className="justify-content-center"),


    ], fluid=True) 

