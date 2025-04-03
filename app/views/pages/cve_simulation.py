from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def cve_simulation_layout():
    return dbc.Container([
        html.H3("Common Vulnerabilities and Exposures Simulation", className="text-center mt-4"),
    ], fluid=True)
