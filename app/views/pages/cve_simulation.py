from dash import html, dcc
import dash_bootstrap_components as dbc
from app.services.cve_service import CVEService
import pandas as pd

# ----------------------------
# Style
# ----------------------------

shared_cell_style = {
    "border": "1px solid #dee2e6",
    "padding": "10px",
    "height": "45px",
    "display": "flex",
    "alignItems": "center",
    "backgroundColor": "white"
}

# ----------------------------
# UI Row Builder
# ----------------------------

def build_cve_row(cve, index):
    return dbc.Row([
        dbc.Col(html.Div(cve["CVE ID"], style=shared_cell_style), width=4),
        dbc.Col(html.Div(cve["Nodes Affected"], style=shared_cell_style), width=3),
        dbc.Col(html.Div(cve["Impact Score"], style=shared_cell_style), width=3),
        dbc.Col(
            html.Div(
                dbc.Button("Patch", id={"type": "patch-btn", "index": index}, size="sm", color="success"),
                style={**shared_cell_style, "border": "none", "justifyContent": "flex-start"}
            ),
            width=2,
        ),
    ], className="g-0")

# ----------------------------
# Layout
# ----------------------------

def cve_simulation_layout():
    df = CVEService.get_unique_cves()

    return dbc.Container([
        dcc.Store(id="patched-cves-store", data=[]),
        dcc.Store(id="all-cves-data", data=df.to_dict("records")),
        dcc.Store(id="current-page", data=0),

        html.H4("CVE Patch Simulation", className="mb-4"),

        # Table Header
        dbc.Row([
            dbc.Col(html.Div("CVE ID", style={**shared_cell_style, "fontWeight": "bold", "backgroundColor": "#f8f9fa"}), width=4),
            dbc.Col(html.Div("Nodes Affected", style={**shared_cell_style, "fontWeight": "bold", "backgroundColor": "#f8f9fa"}), width=3),
            dbc.Col(html.Div("Impact Score", style={**shared_cell_style, "fontWeight": "bold", "backgroundColor": "#f8f9fa"}), width=3),
            dbc.Col(html.Div("", style={**shared_cell_style, "border": "none", "backgroundColor": "transparent"}), width=2),
        ], className="g-0 mb-0"),

        html.Div(id="cve-sim-table-body"),
        html.Div(id="patched-status-msg", className="mt-2 text-success"),

        # Pagination Controls
        dbc.Row([
            dbc.Col(dbc.Button("Previous", id="prev-page-btn", color="secondary"), width="auto"),
            dbc.Col(html.Div(id="page-indicator", className="px-3"), width="auto"),
            dbc.Col(dbc.Button("Next", id="next-page-btn", color="secondary"), width="auto"),
        ], className="mt-4 align-items-center"),
    ], fluid=True)
