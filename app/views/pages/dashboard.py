from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

def dashboard(session_user):
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
                            html.H4("Card 2 Title", className="card-title"),
                            html.P("Content for Card 2 goes here.", className="card-text"),
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
