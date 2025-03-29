from dash import html
import dash_bootstrap_components as dbc

def dashboard(session_user):
    return html.Div([
        # Welcome message
        html.H1(f"Welcome {session_user}! You are logged in.", className="mb-4 text-center"),

        # Dashboard description content
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2("Dashboard Overview", className="mb-3 text-center"),
                    html.P("The CyberGator Dashboard provides an overview of your system’s security status and current Resilience Score.",
                           className="mb-3"),
                    html.Ul([
                        html.Li("Resilience Score: A numerical representation of your system’s ability to withstand and recover from cyber threats."),
                        html.Li("Recent Events: Displays updates related to system changes, environmental risk adjustments, and attack simulations."),
                        html.Li("Quick Navigation: Links to core functionalities such as System Tables, Simulations, and Environmental Factors."),
                    ], className="mb-3"),
                    html.P("The dashboard acts as the control hub for managing cybersecurity assessments and making data-driven improvements.",
                           className="mb-4"),
                ], width=12)
            ])
        ])
    ], id="page-content")