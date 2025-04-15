from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from app.services.data_loader import get_nodes # Load data from Nodes_Complete.json

# Function to load CVE data
def load_cve_data():
    """Extract CVEs, their NVD scores, and affected nodes, fully flattened."""
    nodes_data = get_nodes()  # Load nodes from JSON
    cve_list = []

    for idx, node in enumerate(nodes_data):
        for cve_id, nvd_score in node["CVE_NVD"].items():
            cve_list.append({
                "CVE ID": cve_id,
                "NVD Score": nvd_score,
                "Node ID": node["node_id"],
                "Node Name": node["node_name"],
                "Remove": "❌"
            })
    return cve_list

# Function to get the top 5 most vulnerable CVEs based on NVD Score
def get_top_vulnerable_cves():
    """Fetch and sort the top 5 most vulnerable CVEs by NVD Score."""
    cve_data = load_cve_data()  # Fetch CVE data
    # Convert to DataFrame for easy sorting
    df = pd.DataFrame(cve_data)
    # Sort by NVD Score in descending order
    df_sorted = df.sort_values(by="NVD Score", ascending=False)
    # Get the top 5 most vulnerable CVEs
    top_cves = df_sorted.head(10)
    return top_cves

def dashboard(session_user):

    # Get the actual top 5 most vulnerable CVEs
    top_cves = get_top_vulnerable_cves()  # Fetch the top 5 CVEs

    return html.Div([
        # Welcome message
        html.H1(f"Welcome {session_user}! You are logged in.", className="mb-4 text-center"),

        # Dashboard description content
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2("Dashboard Overview", className="mb-3 text-center"),
                    html.P("The CyberGator Dashboard provides an overview of your system’s current overall Resilence Score.",
                           className="mb-3"),
                    html.Ul([
                        html.Li("Resilience Score: A numerical representation of your system’s ability to withstand and recover from cyber threats."),
                        html.Li("Recent Events: Displays updates related to system changes, environmental risk adjustments, and attack simulations."),
                        html.Li("Quick Navigation: Links to core functionalities such as System Tables, Simulations, and Environmental Factors."),
                    ], className="mb-3"),
                    html.P("The dashboard acts as the control hub for managing cybersecurity assessments and making data-driven improvements.",
                           className="mb-4"),
                ], width=12)
            ]),

            # New Row for Cards
            dbc.Row([
                # First Column
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("System Resilience Score", className="card-title"),
                            html.P("The system's current resilience score represented in a pie chart.", className="card-text"),
                         
                         # Add Pie Chart here
                            dcc.Graph(
                                id="resilience-pie-chart",
                                figure={
                                    "data": [
                                        go.Pie(
                                            labels=["Resilient", "Vulnerable"],
                                            values=[70, 30],  # Replace with your actual data
                                            hole=0.3,  # Makes it a donut chart
                                            hoverinfo="label+percent",
                                            textinfo="percent",
                                        )
                                    ],
                                    "layout": go.Layout(
                                        title="Overall Resilience Score",
                                        showlegend=True,
                                    ),
                                },
                            ),
                        ])
                    ], className="mb-4")
                ], width=6),

                # Second Column
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Top 10 Most Vulnerable CVEs", className="card-title"),
                            html.P("This table will show the top 5 CVEs based on their NVD Score and the nodes they are associated with.", className="card-text"),
                         # Placeholder Table to display top 5 most vulnerable CVEs
                            dash_table.DataTable(
                                id="top-cve-table",
                                columns=[
                                    {"name": "CVE ID", "id": "CVE ID"},
                                    {"name": "NVD Score", "id": "NVD Score"},
                                    {"name": "Node ID", "id": "Node ID"},
                                    {"name": "Node Name", "id": "Node Name"},
                                ],
                                data=top_cves.to_dict("records"),
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left"},
                                page_size=10,
                                filter_action="native",  # Allow filtering of data
                                sort_action="native",  # Allow sorting of columns
                            ),
                        ])
                    ], className="mb-4")
                ], width=6),

                # Third Column
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Card 3 Title", className="card-title"),
                            html.P("Content for Card 3 goes here.", className="card-text"),
                        ])
                    ], className="mb-4")
                ], width=6),

                # Fourth Column
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Card 4 Title", className="card-title"),
                            html.P("Content for Card 4 goes here.", className="card-text"),
                        ])
                    ], className="mb-4")
                ], width=6),
            ])
        ])
    ], id="page-content")
