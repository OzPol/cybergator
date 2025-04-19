import pandas as pd
from collections import defaultdict

from dash import html, dcc, Input, Output, State, callback, ctx, ALL
import dash_bootstrap_components as dbc
from app.services.data_loader import get_nodes

# ----------------------------
# Data + Helpers
# ----------------------------

def get_unique_cves():
    nodes_data = get_nodes()  # Your JSON-based node loader

    cve_summary = defaultdict(lambda: {"NVD Score": 0, "Nodes": set()})

    for node in nodes_data:
        node_id = node["node_id"]
        for cve_id, nvd_score in node.get("CVE_NVD", {}).items():
            cve_summary[cve_id]["NVD Score"] = nvd_score  # assumes consistent score
            cve_summary[cve_id]["Nodes"].add(node_id)

    # Convert to final DataFrame
    records = []
    for cve_id, info in cve_summary.items():
        node_count = len(info["Nodes"])
        nvd = info["NVD Score"]
        records.append({
            "CVE ID": cve_id,
            "Nodes Affected": node_count,
            "Impact Score": round(node_count * nvd, 2),
        })

    df = pd.DataFrame(records)
    df.sort_values("Impact Score", ascending=False, inplace=True)
    return df
            

def build_cve_row(cve, index):
    return dbc.Row([
        dbc.Col(html.P(cve["CVE ID"]), width=4),
        dbc.Col(html.P(cve["Nodes Affected"]), width=3),
        dbc.Col(html.P(cve["Impact Score"]), width=3),
        dbc.Col(dbc.Button("Patch", id={"type": "patch-btn", "index": index}, size="sm", color="success"), width=2),
    ], align="center", className="mb-2")

# ----------------------------
# Layout
# ----------------------------

def cve_simulation_layout():
    df = get_unique_cves()
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
