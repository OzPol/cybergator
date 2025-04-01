from dash import html
import dash_bootstrap_components as dbc

def cve_simulation_layout():
    return dbc.Container([
        html.H2("CVE Simulation Page Loaded", className="text-center text-success mt-5")
    ], fluid=True)
