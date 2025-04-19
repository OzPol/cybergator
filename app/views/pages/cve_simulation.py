import pandas as pd
from dash import html, dcc, Input, Output, State, callback, ctx, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# ----------------------------
# Data + Helpers
# ----------------------------

def get_top_impactful_cves():
    return pd.DataFrame([
        {"CVE ID": "CVE-2023-0001", "nodes_affected": 5, "Impact Score": 9.8},
        {"CVE ID": "CVE-2023-0002", "nodes_affected": 3, "Impact Score": 8.5},
        {"CVE ID": "CVE-2023-0003", "nodes_affected": 2, "Impact Score": 9.2},
    ])

def build_cve_row(cve, index):
    return dbc.Row([
        dbc.Col(html.P(cve["CVE ID"]), width=4),
        dbc.Col(html.P(cve["nodes_affected"]), width=3),
        dbc.Col(html.P(cve["Impact Score"]), width=3),
        dbc.Col(dbc.Button("Patch", id={"type": "patch-btn", "index": index}, size="sm", color="success"), width=2),
    ], align="center", className="mb-2")

# ----------------------------
# Layout
# ----------------------------

def cve_simulation_layout():
    df = get_top_impactful_cves()
    return dbc.Container([
        dcc.Store(id="patched-cves-store", data=[]),
        dcc.Store(id="all-cves-data", data=df.to_dict("records")),

        html.H4("CVE Patch Simulation", className="mb-4"),

        dbc.Row([
            dbc.Col(html.Strong("CVE ID"), width=4),
            dbc.Col(html.Strong("Nodes Affected"), width=3),
            dbc.Col(html.Strong("Impact Score"), width=3),
            dbc.Col(html.Strong("Action"), width=2),
        ], className="border-bottom pb-2 mb-3"),

        html.Div(id="cve-sim-table-body"),
        html.Div(id="patched-status-msg", className="mt-4 text-success")
    ], fluid=True)

# ----------------------------
# Unified Callback with Initial Load Support
# ----------------------------

@callback(
    Output("cve-sim-table-body", "children"),
    Output("patched-status-msg", "children"),
    Output("patched-cves-store", "data"),
    Input("all-cves-data", "data"),
    Input({"type": "patch-btn", "index": ALL}, "n_clicks"),
    State("patched-cves-store", "data"),
)
def update_cve_table(cve_data, patch_clicks, patched_ids):
    triggered_id = ctx.triggered_id
    status_msg = ""

    if triggered_id is None:
        # Initial load — just show table
        filtered = [cve for cve in cve_data if cve["CVE ID"] not in patched_ids]
        rows = [build_cve_row(cve, i) for i, cve in enumerate(filtered)]
        return rows, "", patched_ids

    # Patch button clicked
    if isinstance(triggered_id, dict) and triggered_id.get("type") == "patch-btn":
        index = triggered_id["index"]
        cve_id = cve_data[index]["CVE ID"]
        if cve_id not in patched_ids:
            patched_ids.append(cve_id)
            status_msg = f"Patched {cve_id}"

    # Updated table after patch
    filtered = [cve for cve in cve_data if cve["CVE ID"] not in patched_ids]
    rows = [build_cve_row(cve, i) for i, cve in enumerate(filtered)]
    return rows, status_msg, patched_ids
