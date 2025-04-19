import os
import json
import dash
from dash import html, dcc, Output, Input, State, callback, ctx
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from app.services.cvss_service import (
    extract_unique_cves,
    fetch_cvss_metadata,
    write_cvss_cache,
    CVSS_CACHE_PATH
)

from dotenv import load_dotenv
load_dotenv()

# Load system data
with open("app/data/json/Nodes_Complete.json", "r") as f:
    NODES_DATA = json.load(f)

# Callback to Load Graph on Page Load
@callback(
    Output("sim-system-graph", "elements"),
    Output("sim-system-graph-data", "data"),
    Input("sim-system-graph", "id")
)
def load_sim_system_graph(_):
    elements = generate_sim_system_graph_elements(NODES_DATA)
    return elements, elements


# Callback to Hover Info Panel
@callback(
    Output("sim-node-hover-info", "children"),
    Input("sim-system-graph", "mouseoverNodeData")
)
def show_node_hover_info(data):
    if not data:
        return html.Div("Hover over a node to see its metadata.")
    
    return html.Div([
        html.H5(f"Node ID: {data['id']}"),
        html.P(f"Node Type: {data.get('node_type', 'N/A')}"),
        html.P(f"Critical Functions: {data.get('critical_functions', 'None')}"),
        html.P(f"CVE Count: {data.get('cve_count', 0)}"),
        html.P(f"Total NVD Score: {data.get('cve_score', 0)}")
    ])

# Callback to Populate Dropdown for CVE Selection
#  will load CVE options based on what's actually in the graph data
@callback(
    Output("sim-cve-selector", "options"),
    Input("sim-system-graph-data", "data")
)
def populate_cve_dropdown(graph_data):
    seen = set()
    options = []
    for item in graph_data:
        if "data" in item and "CVE" in item["data"]:
            for cve in item["data"]["CVE"]:
                if cve not in seen:
                    seen.add(cve)
                    options.append({"label": cve, "value": cve})
    return sorted(options, key=lambda x: x["label"])

# Callback to fetch and store the CVSS data
@callback(
    Output("fetch-cvss-status", "children"),
    Output("fetch-cvss-btn", "disabled"),
    Input("fetch-cvss-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_fetch_cvss(n_clicks):
    try:
        cve_list = extract_unique_cves(NODES_DATA)
        results = fetch_cvss_metadata(cve_list)
        write_cvss_cache(CVSS_CACHE_PATH, results)
        msg = f"Fetched metadata for {len(results)} CVEs. Data saved to {CVSS_CACHE_PATH}"
        return msg, False
    except Exception as e:
        return f"Error: {str(e)}", False

# Callback to Update Node Classes Based on Selected CVE
@callback(
    Output("sim-system-graph", "elements", allow_duplicate=True),
    Input("sim-cve-selector", "value"),
    State("sim-system-graph-data", "data"),
    prevent_initial_call=True
)
def mark_entry_nodes(selected_cve, graph_data):
    """
    Highlight nodes that contain the CVE
    Scan node["CVE"]
    If it contains the selected CVE → it's a candidate entry node
    Apply a visual style: red colored node in this case
    but later can be pulsing animation, bigger size, etc.
    """
    if not selected_cve:
        return graph_data

    updated = []
    for el in graph_data:
        if "source" in el.get("data", {}):  # It's an edge
            updated.append(el)
        else:
            node = el["data"]
            classes = "entry-cve" if selected_cve in node.get("CVE", []) else ""
            updated.append({
                "data": node,
                "classes": classes
            })
    return updated


# Load CVSS metadata once at the top of apt_simulation.py
with open(CVSS_CACHE_PATH, "r") as f:
    CVSS_METADATA = json.load(f)
    
def extract_cvss_filter_options(cvss_metadata):
    av_set = set()
    pr_set = set()
    ui_set = set()
    vector_set = set()      #  To enable vector string & score-based logic later

    for data in cvss_metadata.values():
        if isinstance(data, dict) and not data.get("error"):
            av = data.get("attack_vector")
            pr = data.get("privileges_required")
            ui = data.get("user_interaction")
            vector = data.get("vector_string")

            if av: av_set.add(av)
            if pr: pr_set.add(pr)
            if ui: ui_set.add(ui)
            if vector: vector_set.add(vector)

    return {
        "av_options": [{"label": val, "value": val} for val in sorted(av_set)],
        "pr_options": [{"label": val, "value": val} for val in sorted(pr_set)],
        "ui_options": [{"label": val, "value": val} for val in sorted(ui_set)],
        "vector_options": sorted(vector_set),
    }

# defining controls:
CVSS_FILTER_OPTIONS = extract_cvss_filter_options(CVSS_METADATA)



""" 
# We can tokenize vector_string like this:

# def parse_cvss_vector(vector):
#    return dict(item.split(":") for item in vector.split("/") if ":" in item)

This turns:
    "AV:L/AC:L/Au:N/C:C/I:C/A:C"
into:
    {
        "AV": "L",
        "AC": "L",
        "Au": "N",
        "C": "C",
        "I": "C",
        "A": "C"
    }
Can be used for:
Scoring formulas
Heatmaps
Probabilistic impact modeling
Condition-based traversal rules
"""



# Helper to Generate Cytoscape Elements from Node Data
def generate_sim_system_graph_elements(nodes_data):
    elements = []

    color_map = {
        "server": "#FFA500",             # Orange
        "workstation": "#2ECC71",        # Light green
        "san": "#DDA0DD",                # Plum
        "san_archive": "#9370DB",        # Medium Purple
        "san_archive_backup": "#708090", # Slate Gray
        "switch": "#ADD8E6",             # Light Blue
        "router": "#FFA07A",             # Light Orange
        "firewall": "#FF6347",           # Tomato Red
    }

    for node in nodes_data:
        node_id = node.get("node_id")
        label = node.get("node_name", node_id)
        node_type = node.get("node_type", "unknown").lower()
        functions = node.get("critical_functions", [])
        connected = node.get("connected_to", [])
        cves = node.get("CVE", [])
        cve_scores = node.get("CVE_NVD", {})
        risk = node.get("risk_factor", "Unknown")
        backup_role = node.get("backup_role")
        redundancy = node.get("redundancy", False)
        switch_dependency = node.get("switch_dependency", False)
        critical_data = node.get("critical_data_stored", False)
        data_redundancy = node.get("data_redundancy", "Unknown")
        penalty = node.get("resilience_penalty", 0.0)

        node_data = {
            "id": node_id,
            "label": f"{label}\nCVEs: {len(cves)}",
            "node_name": label,
            "node_type": node_type,
            "critical_functions": functions,
            "cve_count": len(cves),
            "cve_score": sum(cve_scores.values()),
            "CVE": cves,
            "CVE_NVD": cve_scores,
            "connected_to": connected,
            "risk_factor": risk,
            "backup_role": backup_role,
            "redundancy": redundancy,
            "switch_dependency": switch_dependency,
            "critical_data_stored": critical_data,
            "data_redundancy": data_redundancy,
            "resilience_penalty": penalty,
            "color": color_map.get(node_type, "gray")
        }

        elements.append({
            "data": node_data
        })

        for target in node.get("connected_to", []):
            elements.append({
                "data": {
                    "source": node_id,
                    "target": target
                }
            })

    return elements

# Layout 
def simulation_apt_layout():
    return html.Div([
        dcc.Store(id="sim-system-graph-data"),
        dcc.Store(id="sim-hover-node-info"),
        dcc.Store(id="sim-cve-metadata"),

        html.H3("System Graph View", style={"marginTop": "20px"}),
        
        # Fetch CVSS Metadata Button API CALL to NVD
        dbc.Button(
            "Fetch CVSS Metadata",
            id="fetch-cvss-btn",
            color="primary",
            className="mb-3"
        ),
        html.Div(id="fetch-cvss-status", style={"marginBottom": "20px"}),
        
        # CVE Selection Section
        dbc.Row([
            dbc.Card([
                dbc.CardHeader("Select CVE for Attack Simulation"),
                dbc.CardBody([
                    html.Label("Select a CVE to simulate attack propagation:", style={"fontWeight": "bold"}),
                    dcc.Dropdown(
                        id="sim-cve-selector",
                        options=[],
                        placeholder="Select CVE...",
                        style={"width": "100%", "zIndex": 1000}  # Boost z-index here
                    ),
                    html.Div(id="sim-cve-description", style={"marginTop": "10px", "fontStyle": "italic", "color": "#555"})
                ])
            ], className="mb-4", style={"width": "30%", "marginBottom": "40px", "zIndex": 999}, color="light")
        ]),
        
        # Graph Section
        cyto.Cytoscape(
            id="sim-system-graph",
            layout={
                "name": "breadthfirst",
                "spacingFactor": 2,
                "padding": 20,
                "animate": True,
            },
            style={ "width": "100%", "height": "800px",                     
                    "border": "2px solid #007BFF",
                    "borderRadius": "10px",
                    "padding": "10px",
                    "marginTop": "10px",
                    "marginBottom": "20px",
                    "backgroundColor": "#f9f9f9"},
            elements=[],
            minZoom=0.5,
            maxZoom=1.05,
            zoomingEnabled=True,
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "background-color": "data(color)",
                        "width": 50,
                        "height": 50,
                        "text-valign": "center",
                        "text-halign": "center",
                        "font-size": 10,
                        "color": "#000",
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#444",
                        "width": 2,
                    },
                },
                {
                    "selector": ".entry-cve",
                    "style": {
                        "border-color": "#000",
                        "border-width": 5,
                        "background-color": "#FF0000",
                        "width": 70,
                        "height": 70,
                    },
                }
            ]
        ),
        
        # Node Hover Info Panel
        html.Div([
            dbc.Card([
                    dbc.CardBody(id="sim-node-hover-info")
                ], style={"width": "30%", "marginBottom": "20px"}, color="light")
            ], style={"marginTop": "40px"}),
        
        # CVSS Filtering Controls Section
        dbc.Card([
            dbc.CardHeader("CVSS Filtering Controls"),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Label("Attack Vector"),
                        dcc.Dropdown(
                            id="sim-filter-av",
                            options=CVSS_FILTER_OPTIONS["av_options"],
                            multi=True,
                            value=[opt["value"] for opt in CVSS_FILTER_OPTIONS["av_options"] if opt["value"] in ["NETWORK", "ADJACENT_NETWORK"]]
                        )
                    ]),
                    dbc.Col([
                        html.Label("Privileges Required"),
                        dcc.Dropdown(
                            id="sim-filter-pr",
                            options=CVSS_FILTER_OPTIONS["pr_options"],
                            multi=True,
                            value=[opt["value"] for opt in CVSS_FILTER_OPTIONS["pr_options"] if opt["value"] in ["NONE", "LOW", "NA"]]
                        )
                    ]),
                    dbc.Col([
                        html.Label("User Interaction"),
                        dcc.Dropdown(
                            id="sim-filter-ui",
                            options=CVSS_FILTER_OPTIONS["ui_options"],
                            multi=True,
                            value=[opt["value"] for opt in CVSS_FILTER_OPTIONS["ui_options"] if opt["value"] in ["NONE", "NA"]]
                        )
                    ]),
                ])
            ])
        ], className="mb-4"),

        # Run Simulation Button Section
        html.Div([
            dbc.Button("Run Simulation", id="sim-run-btn", color="primary", className="mb-3"),
        ], style={"textAlign": "left"}),

        # Simulation Results Card
        dbc.Card([
            dbc.CardHeader("Simulation Results"),
            dbc.CardBody(html.Div(id="sim-results-table"))
        ], style={"marginBottom": "50px"})
    ])
