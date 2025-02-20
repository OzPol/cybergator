import dash
import os
from dash.dependencies import Input, Output
import dash_cytoscape as cyto
from dash import dcc, html, Input, Output
from test_neo4j_queries import get_network_graph

# Create Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

NEO4J_BROWSER_URL = "https://92da8f26.databases.neo4j.io/browser/"
# Define styles
HEADER_STYLE = {
    "background-color": "#FA4616",  # UF Orange
    "height": "80px",
    "color": "white",
    "text-align": "center",
    "font-size": "40px",
    "font-weight": "bold",
    "padding": "20px",  # Remove extra spacing
    "margin": "0px", 
    "display": "flex",
    "align-items": "center",
    "justify-content": "center"
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20%",
    "padding": "20px",
    "background-color": "#0021A5",  # UF Blue
    "color": "white",
    "font-size": "22px",
}

CONTENT_STYLE = {
    "margin-left": "22%", 
    "padding": "20px",
    "font-size": "18px",
}

BUTTON_STYLE = {
    "width": "100%",
    "padding": "10px",
    "margin": "5px 0",
    "border": "none",
    "border-radius": "5px",
    "background-color": "#FA4616",  # UF Orange
    "color": "white",
    "font-size": "18px",
    "cursor": "pointer",
}

# App Layout
app.layout = html.Div([
    
    dcc.Location(id='url', refresh=False),
    html.Div("CyberGator", style=HEADER_STYLE),
    
    html.Div([
        html.H2("Dashboard", style={"font-size": "32px", "margin-bottom": "20px", "text-align": "center"}),
        dcc.Link(html.Button("System Graph", style=BUTTON_STYLE), href="/"),
        dcc.Link(html.Button("CVE Simulation", style=BUTTON_STYLE), href="/cve-simulation"),
        dcc.Link(html.Button("FSM Simulation", style=BUTTON_STYLE), href="/fsm-simulation"),
        dcc.Link(html.Button("APT Attack Simulation", style=BUTTON_STYLE), href="/apt-attack-simulation"),
        dcc.Link(html.Button("Environmental Risk Factors", style=BUTTON_STYLE), href="/environment-risk"),
        dcc.Link(html.Button("Holistic Simulation", style=BUTTON_STYLE), href="/holistic-simulation"),
        dcc.Link(html.Button("Neo4j Graph", style=BUTTON_STYLE), href="/neo4j-graph"),  
    ], style=SIDEBAR_STYLE),
    
    html.Div([
        html.Img(src="/assets/system.png", style={'width': '100%', 'height': 'auto'}),
    ], style=CONTENT_STYLE),

    html.Div(id="page-content", style=CONTENT_STYLE)  
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/neo4j-graph":
        return html.Div([
            html.H1("Neo4j Graph Visualization", style={"text-align": "center"}),

                cyto.Cytoscape(
                    id="cytoscape-network",
                    layout={"name": "cose"},  # Auto-organizing graph
                    style={"width": "100%", "height": "600px"},
                    elements=get_network_graph(),  # Load elements from Neo4j

                    stylesheet=[  # styles for nodes and edges

                    ]
                )
        ])

if __name__ == '__main__':
    app.run_server(debug=True)