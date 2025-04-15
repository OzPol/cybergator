from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from app.services.data_loader import get_nodes # Load data from Nodes_Complete.json
import requests

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


# Function to get the most impactful CVE (aggregated by node count * NVD score)
def get_most_impactful_cve():
    """Fetch and calculate the most impactful CVE based on node count * NVD Score."""
    cve_data = load_cve_data()  # Fetch CVE data
    # Convert to DataFrame for easy manipulation
    df = pd.DataFrame(cve_data)

    # Group by CVE ID and calculate the number of nodes affected by each CVE
    cve_impact = df.groupby('CVE ID').agg(
        nodes_affected=('Node ID', 'nunique'),
        nvd_score=('NVD Score', 'first')
    ).reset_index()

    # Calculate the impact score as (number of nodes affected * NVD Score)
    cve_impact['Impact Score'] = cve_impact['nodes_affected'] * cve_impact['nvd_score']

    # Sort by Impact Score in descending order to get the most impactful CVE
    most_impactful_cve = cve_impact.sort_values(by="Impact Score", ascending=False).head(3)

    return most_impactful_cve

def get_resilience_score():
    """Fetch the system resilience score from the API."""
    try:
        response = requests.get("http://localhost:8000/api/resilience")
        if response.status_code == 200:
            data = response.json()
            return round(data["system_resilience_score"], 4)
    except Exception as e:
        print(f"Error fetching resilience score: {str(e)}")
    return None

def dashboard(session_user):

    # Get the actual top 10 most vulnerable CVEs
    top_cves = get_top_vulnerable_cves()  # Fetch the top 10 CVEs

    # Get the most impactful CVE
    top_impactful_cves = get_most_impactful_cve()  # Fetch the most impactful CVEs

    # Get the system resilience score
    resilience_score = get_resilience_score()

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
                                            values=[resilience_score, 100 - resilience_score],  # Replace with your actual data
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
                            html.H4("Top 10 Most Vulnerable Individual CVEs", className="card-title"),
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

                # Third Column: Top 3 Most Impactful CVEs Table (Aggregated by Node Count * NVD Score)
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Top 3 Most Impactful CVEs", className="card-title"),
                            html.P("This table shows the top 3 CVEs based on the aggregation of the number of nodes affected and the NVD Score.", className="card-text"),
                            # Top 3 most impactful CVE data in the table
                            dash_table.DataTable(
                                id="impactful-cve-table",
                                columns=[
                                    {"name": "CVE ID", "id": "CVE ID"},
                                    {"name": "Nodes Affected", "id": "nodes_affected"},
                                    {"name": "Impact Score", "id": "Impact Score"},
                                ],
                                data=top_impactful_cves.to_dict("records"),
                                style_table={"overflowX": "auto"},
                                style_cell={"textAlign": "left"},
                                page_size=3,  # Display top 3 impactful CVEs
                                filter_action="native",  # Allow filtering of data
                                sort_action="native",  # Allow sorting of columns
                            ),
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
