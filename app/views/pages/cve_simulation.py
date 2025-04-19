import pandas as pd
from collections import defaultdict
from dash import html, dcc, Input, Output, State, callback, ctx, ALL
import dash_bootstrap_components as dbc
from app.services.data_loader import get_nodes, save_nodes_data

# ----------------------------
# Data + Helpers
# ----------------------------

def get_unique_cves():
    nodes_data = get_nodes()
    cve_summary = defaultdict(lambda: {"NVD Score": 0, "Nodes": set()})

    for node in nodes_data:
        node_id = node["node_id"]
        for cve_id, nvd_score in node.get("CVE_NVD", {}).items():
            cve_summary[cve_id]["NVD Score"] = nvd_score
            cve_summary[cve_id]["Nodes"].add(node_id)

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

def patch_cve(cve_id):
    nodes_data = get_nodes()
    for node in nodes_data:
        if cve_id in node.get("CVE", []):
            node["CVE"].remove(cve_id)
            node.get("CVE_NVD", {}).pop(cve_id, None)
    save_nodes_data(nodes_data)

shared_cell_style = {
    "border": "1px solid #dee2e6",
    "padding": "10px",
    "height": "45px",
    "display": "flex",
    "alignItems": "center",
    "backgroundColor": "white"
}

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
    ], className="g-0")  # No gutter between columns

# ----------------------------
# Layout
# ----------------------------

def cve_simulation_layout():
    df = get_unique_cves()

    return dbc.Container([
        dcc.Store(id="patched-cves-store", data=[]),
        dcc.Store(id="all-cves-data", data=df.to_dict("records")),
        dcc.Store(id="current-page", data=0),

        html.H4("CVE Patch Simulation", className="mb-4"),

        # Header Row
        dbc.Row([
            dbc.Col(html.Div("CVE ID", style={**shared_cell_style, "fontWeight": "bold", "backgroundColor": "#f8f9fa"}), width=4),
            dbc.Col(html.Div("Nodes Affected", style={**shared_cell_style, "fontWeight": "bold", "backgroundColor": "#f8f9fa"}), width=3),
            dbc.Col(html.Div("Impact Score", style={**shared_cell_style, "fontWeight": "bold", "backgroundColor": "#f8f9fa"}), width=3),
            dbc.Col(html.Div("", style={**shared_cell_style, "border": "none", "backgroundColor": "transparent"}), width=2),
        ], className="g-0 mb-0"),

        html.Div(id="cve-sim-table-body"),
        html.Div(id="patched-status-msg", className="mt-2 text-success"),

        # Pagination controls
        dbc.Row([
            dbc.Col(dbc.Button("Previous", id="prev-page-btn", color="secondary"), width="auto"),
            dbc.Col(html.Div(id="page-indicator", className="px-3"), width="auto"),
            dbc.Col(dbc.Button("Next", id="next-page-btn", color="secondary"), width="auto"),
        ], className="mt-4 align-items-center"),
    ], fluid=True)

# ----------------------------
# Callbacks
# ----------------------------

@callback(
    Output("cve-sim-table-body", "children"),
    Output("patched-status-msg", "children"),
    Output("patched-cves-store", "data"),
    Output("page-indicator", "children"),
    Output("prev-page-btn", "disabled"),
    Output("next-page-btn", "disabled"),
    Input("all-cves-data", "data"),
    Input({"type": "patch-btn", "index": ALL}, "n_clicks"),
    Input("prev-page-btn", "n_clicks"),
    Input("next-page-btn", "n_clicks"),
    State("patched-cves-store", "data"),
    State("current-page", "data"),
)
def update_table(data, patch_clicks, prev_clicks, next_clicks, patched, current_page):
    page_size = 10
    triggered = ctx.triggered_id
    status_msg = ""

    filtered = [cve for cve in data if cve["CVE ID"] not in patched]
    total_pages = max((len(filtered) - 1) // page_size + 1, 1)

    # Handle patch
    if isinstance(triggered, dict) and triggered.get("type") == "patch-btn":
        index = triggered["index"]
        global_index = current_page * page_size + index
        if 0 <= global_index < len(filtered):
            cve_id = filtered[global_index]["CVE ID"]
            if cve_id not in patched:
                patched.append(cve_id)
                patch_cve(cve_id)
                status_msg = f"Patched {cve_id}."

        filtered = [cve for cve in data if cve["CVE ID"] not in patched]
        total_pages = max((len(filtered) - 1) // page_size + 1, 1)

    # Pagination
    if triggered == "prev-page-btn" and current_page > 0:
        current_page -= 1
    elif triggered == "next-page-btn" and current_page < total_pages - 1:
        current_page += 1

    paginated = filtered[current_page * page_size: (current_page + 1) * page_size]
    rows = [build_cve_row(cve, i) for i, cve in enumerate(paginated)]

    return (
        rows,
        status_msg,
        patched,
        f"Page {current_page + 1} of {total_pages}",
        current_page == 0,
        current_page >= total_pages - 1,
    )

@callback(
    Output("current-page", "data"),
    Input("prev-page-btn", "n_clicks"),
    Input("next-page-btn", "n_clicks"),
    State("current-page", "data"),
    prevent_initial_call=True
)
def update_page_store(prev_clicks, next_clicks, page):
    triggered = ctx.triggered_id
    if triggered == "prev-page-btn" and page > 0:
        return page - 1
    elif triggered == "next-page-btn":
        return page + 1
    return page
