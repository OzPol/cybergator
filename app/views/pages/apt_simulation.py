import os
import json
import dash
from dash import dash_table
from dash import html, dcc, Output, Input, State, callback, ctx
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
from collections import deque
import networkx as nx
from app.services.cvss_service import (extract_unique_cves, fetch_cvss_metadata,
    write_cvss_cache, CVSS_CACHE_PATH )
from app.services.data_loader import get_software_inventory, get_software_cves, get_critical_functions
from app.services.constraints import ( is_valid_entry_node, can_traverse_rack_boundary,
    has_access_to_node, nodes_share_vulnerable_software, build_privilege_lookup_from_type)

PRIVILEGE_LOOKUP = build_privilege_lookup_from_type()


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
We can tokenize vector_string like this:
    def parse_cvss_vector(vector):
        return dict(item.split(":") for item in vector.split("/") if ":" in item)
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

@callback(
    Output("sim-results-table", "children"),
    Input("sim-run-btn", "n_clicks"),
    State("sim-cve-selector", "value"),
    State("sim-system-graph-data", "data"),
    State("sim-filter-av", "value"),
    State("sim-filter-pr", "value"),
    State("sim-filter-ui", "value"),
    State("sim-filter-score", "value"),
    prevent_initial_call=True
)
def run_cve_simulation(n_clicks, selected_cve, graph_data, av_choices, pr_choices, ui_choices, score_thresh):
    if not selected_cve:
        return html.Div("Please select a CVE to run the simulation.")

    # Load CVSS Metadata
    with open(CVSS_CACHE_PATH, "r") as f:
        metadata = json.load(f)

    passing_nodes = []
    for item in graph_data:
        data = item.get("data", {})
        if selected_cve in data.get("CVE", []):
            cve_meta = metadata.get(selected_cve, {})
            av = cve_meta.get("attack_vector")
            pr = cve_meta.get("privileges_required")
            ui = cve_meta.get("user_interaction")
            if av in av_choices and pr in pr_choices and ui in ui_choices:
                passing_nodes.append({
                    "Node ID": data["id"],
                    "Type": data.get("node_type", "Unknown"),
                    "CVEs": ", ".join(data.get("CVE", [])),
                    "Total Score": data.get("cve_score", 0),
                    "Attack Vector": av,
                    "Privileges Required": pr,
                    "User Interaction": ui,
                    "Vector String": cve_meta.get("vector_string")
                })

    if not passing_nodes:
        return html.Div("No entry nodes passed the CVSS filter.", style={"color": "red"})

    # Build Table
    table = dbc.Table([
        html.Thead(html.Tr([html.Th(k) for k in passing_nodes[0].keys()])),
        html.Tbody([
            html.Tr([html.Td(row[k]) for k in row]) for row in passing_nodes
        ])
    ], bordered=True, striped=True, hover=True)

    return table

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

        html.H3("APT Simulation", className="text-center"),
        
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
                },
                {
                    "selector": ".reachable",
                    "style": {
                        "background-color": "#FF4136",
                        "line-color": "#FF4136",
                        "border-width": 3,
                        "width": 65,
                        "height": 65
                    }
                },
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
                    dbc.Col([
                        html.Label("Minimum CVSS Score"),
                        dcc.Input(
                            id="sim-filter-score",
                            type="number",
                            min=0.1,
                            max=10.0,
                            step=0.1,
                            value=0.1,
                            style={"width": "100%"}
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
        ], style={"marginBottom": "50px"}),
        
        # Attack Log Section
        dbc.Card([
            dbc.CardHeader("Attack Log"),
            dbc.CardBody([
                dash_table.DataTable(
                    id="sim-attack-log",
                    columns=[
                        {"name": "Entry Node", "id": "Entry Node"},
                        {"name": "Reachable Nodes", "id": "Reachable Nodes"}
                    ],
                    style_cell={
                        "textAlign": "left",
                        "whiteSpace": "pre-line",
                        "height": "auto",
                        "fontSize": 12
                    },
                    style_table={"overflowX": "auto"},
                    page_size=10
                )
            ])
        ], style={"marginTop": "30px", "marginBottom": "50px"}),
        
        # Full Attack Graph Header 
        dbc.Card([
            dbc.CardHeader("CVE Based Attack Propagation Graph for All CVEs"),
        ], style={"marginBottom": "5px", "width": "30%"}),
        # Full Attack Graph Section
        cyto.Cytoscape(
            id="sim-attack-graph",
            layout={"name": "breadthfirst",
                    "padding": 20,
                    "animate": True,
                },
            style={"width": "100%",
                    "height": "700px", 
                    "marginTop": "5px",
                    "marginBottom": "50px",                     
                    "border": "2px solid #007BFF",
                    "borderRadius": "10px",
                    "padding": "10px",
                    "backgroundColor": "#f9f9f9"
                },
            elements=[],
            minZoom=0.5,
            maxZoom=1.05,
            zoomingEnabled=True,
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "background-color": "#FF4136",
                        "label": "data(label)",
                        "width": 60,
                        "height": 60
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#FF4136",
                        "width": 2
                    }
                }
            ]
        ), 
        dbc.Card([
            dbc.CardBody(id="sim-attack-node-hover-info")
        ], style={"width": "30%", "marginTop": "10px", "marginBottom": "20px"}, color="light")
    ])


def build_attack_graph(graph_data, entry_node_ids, score_threshold=0.0):
    """
    Builds an attack graph starting from filtered entry nodes.

    This simulates attacker reachability by traversing the system graph topology
    starting from nodes that match the selected CVE and CVSS filters.

    For each entry node:
    1. Start traversal from the node (BFS).
    2. Only follow edges to connected nodes that also have at least one CVE
        with a score above a defined threshold (i.e., exploitable).
    3. Continue traversal recursively until no more valid nodes can be reached.
    4. Collect all visited nodes as reachable from that entry point.

    Returns:
    - A list of all reachable node IDs (for graph coloring/labeling).
    - A list of logs showing which nodes were reached from each entry node.
    
    ---
    
    This can be used to visualize attack paths and assess the system's resilience
    against potential attacks.
    It can be done using DFS or BFS. In this case, BFS is used for simplicity.
    
    BFS explores nodes level-by-level — simulates how attacks spread in real time 
    (e.g., “first compromise neighbors, then neighbors of neighbors”).
    It builds shortest-path reachability trees
    which can be used to show minimum number of steps to compromise or
    to assign weights/costs/delays (e.g., for probabilistic or time-aware attack models)
    Most real-world attack propagation tools (like TVA, NetSPA)
    use a BFS-like logic for phase-based simulation.

    """
    G = nx.DiGraph()
    node_lookup = {}

    for el in graph_data:
        if "data" in el and "id" in el["data"]:
            node_id = el["data"]["id"]
            G.add_node(node_id, **el["data"])
            node_lookup[node_id] = el["data"]

    for el in graph_data:
        d = el.get("data", {})
        if "source" in d and "target" in d:
            src = d["source"]
            tgt = d["target"]
            src_score = max(G.nodes[src].get("CVE_NVD", {}).values(), default=0)
            tgt_score = max(G.nodes[tgt].get("CVE_NVD", {}).values(), default=0)
            if src_score >= score_threshold and tgt_score >= score_threshold:
                G.add_edge(src, tgt)

    attack_subgraph = nx.DiGraph()
    reachable = set()
    attack_log = []

    for entry in entry_node_ids:
        if entry not in G:
            continue

        visited = set()
        queue = deque([entry])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            reachable.add(current)

            for neighbor in G.successors(current):
                queue.append(neighbor)
                attack_subgraph.add_edge(current, neighbor)

        attack_log.append({
            "entry": entry,
            # "reachable": sorted(visited)
            "reachable": [
                f"{nid} ({data.get('node_name', '')}, {data.get('node_type', '')}, "
                f"CVEs: {len(data.get('CVE', []))}, Score: {sum(data.get('CVE_NVD', {}).values()):.1f})"
                for nid in sorted(visited)
                if (data := node_lookup.get(nid))
            ]
        })

    return list(reachable), attack_log, attack_subgraph

def format_attack_log(attack_log, node_lookup):
    """Enriches and formats the attack log for UI display."""
    formatted = []
    for entry in attack_log:
        entry_id = entry["entry"]
        reachable = entry["reachable"]

        entry_node = node_lookup.get(entry_id, {})
        entry_label = f"{entry_id} ({entry_node.get('node_name', 'N/A')}, {entry_node.get('node_type', 'N/A')}, CVEs: {len(entry_node.get('CVE', []))}, Score: {round(sum(entry_node.get('CVE_NVD', {}).values()), 1)})"

        reach_labels = []
        for nid in reachable:
            n = node_lookup.get(nid, {})
            label = f"{nid} ({n.get('node_name', 'N/A')}, {n.get('node_type', 'N/A')}, CVEs: {len(n.get('CVE', []))}, Score: {round(sum(n.get('CVE_NVD', {}).values()), 1)})"
            reach_labels.append(label)

        formatted.append({
            "Entry Node": entry_label,
            "Attack Reach": reach_labels
        })

    return formatted

@callback(
    Output("sim-attack-graph", "elements"),
    Output("sim-attack-log", "data"),
    Input("sim-run-btn", "n_clicks"),
    State("sim-system-graph-data", "data"),
    State("sim-filter-av", "value"),
    State("sim-filter-pr", "value"),
    State("sim-filter-ui", "value"),
    State("sim-filter-score", "value"),
    prevent_initial_call=True
)
def run_full_attack_graph_simulation(n_clicks, graph_data, av_choices, pr_choices, ui_choices, score_thresh):
    import networkx as nx
    from collections import deque
    import json

    # Load metadata and software info
    with open(CVSS_CACHE_PATH, "r") as f:
        metadata = json.load(f)

    software_inventory = get_software_inventory()
    software_map = {}
    for row in software_inventory:
        node_id = row["node_id"]
        swid = row["software_id"]
        software_map.setdefault(node_id, set()).add(swid)

    PRIVILEGE_LOOKUP = build_privilege_lookup_from_type()

    # Build graph
    node_lookup = {}
    G = nx.DiGraph()
    for el in graph_data:
        if "data" in el and "id" in el["data"]:
            data = el["data"]
            nid = data["id"]
            node_lookup[nid] = data
            data["software_ids"] = list(software_map.get(nid, []))
            G.add_node(nid, **data)

    for el in graph_data:
        d = el.get("data", {})
        if "source" in d and "target" in d:
            G.add_edge(d["source"], d["target"])

    # Step 1: Find all valid (node, CVE) entry points
    entry_points = []
    for nid, node in node_lookup.items():
        for cve in node.get("CVE", []):
            cve_meta = metadata.get(cve, {})
            if not is_valid_entry_node(node, cve, cve_meta):
                continue
            if cve_meta.get("attack_vector") not in av_choices:
                continue
            if cve_meta.get("privileges_required") not in pr_choices:
                continue
            if cve_meta.get("user_interaction") not in ui_choices:
                continue
            score = cve_meta.get("base_score", 0)
            if score < score_thresh:
                continue
            entry_points.append((nid, cve, cve_meta))

    if not entry_points:
        return [], [{"Entry Node": "None", "Reachable Nodes": "No CVEs passed the filters."}]

    # Step 2: Traverse from each entry point
    attack_graph = nx.DiGraph()
    attack_log = []

    for entry_node, cve_id, cve_meta in entry_points:
        if entry_node not in G:
            continue

        visited = set()
        q = deque([entry_node])
        while q:
            current = q.popleft()
            if current in visited:
                continue
            visited.add(current)

            for neighbor in G.successors(current):
                src_node = node_lookup.get(current)
                tgt_node = node_lookup.get(neighbor)
                if not src_node or not tgt_node:
                    continue

                src_score = max(src_node.get("CVE_NVD", {}).values(), default=0)
                tgt_score = max(tgt_node.get("CVE_NVD", {}).values(), default=0)
                if src_score < score_thresh or tgt_score < score_thresh:
                    continue
                
                """
                if not can_traverse_rack_boundary(src_node, tgt_node, cve_meta):
                    continue
                if not has_access_to_node(PRIVILEGE_LOOKUP.get(current), neighbor):
                    continue
                if not nodes_share_vulnerable_software(src_node, tgt_node, software_inventory):
                    continue
                """
                rack_ok = can_traverse_rack_boundary(src_node, tgt_node, cve_meta)
                priv_ok = has_access_to_node(PRIVILEGE_LOOKUP.get(current), neighbor)
                sw_ok = nodes_share_vulnerable_software(src_node, tgt_node, software_inventory)

                if not (( rack_ok or sw_ok) and  priv_ok ):
                    continue


                q.append(neighbor)
                attack_graph.add_edge(current, neighbor)

        visited.discard(entry_node)  # don't self-report
        formatted = []
        for nid in sorted(visited):
            data = node_lookup.get(nid, {})
            formatted.append(f"{nid} ({data.get('node_name', 'N/A')}, {data.get('node_type', 'N/A')}, "
                            f"CVEs: {len(data.get('CVE', []))}, Score: {round(sum(data.get('CVE_NVD', {}).values()), 1)})")

        attack_log.append({
            "Entry Node": f"{entry_node} ({node_lookup[entry_node].get('node_name', '')}) - {cve_id}",
            "Reachable Nodes": "\n".join(formatted) if formatted else "None"
        })

    # Step 3: Format Cytoscape output
    elements = []
    added_nodes = set()
    for src, tgt in attack_graph.edges():
        for nid in [src, tgt]:
            if nid not in added_nodes:
                node = node_lookup[nid]
                # elements.append({"data": node, "classes": "reachable"})
                node_copy = node.copy()
                node_copy["label"] = node.get("node_id", node["id"])
                elements.append({
                    "data": node_copy,
                    "classes": "reachable"
                })
                added_nodes.add(nid)
        elements.append({"data": {"source": src, "target": tgt}})
        attack_log.sort(key=lambda x: x["Reachable Nodes"] == "None")

    return elements, attack_log

@callback(
    Output("sim-attack-node-hover-info", "children"),
    Input("sim-attack-graph", "mouseoverNodeData")
)
def show_sim_attack_hover_info(data):
    if not data:
        return html.Div("Hover over a node in the attack graph to see details.")

    return html.Div([
        html.H5(f"Node Name: {data.get('node_name', data['id'])}"),
        html.P(f"Node ID: {data.get('id')}"),
        html.P(f"Type: {data.get('node_type', 'N/A')}"),
        html.P(f"CVEs: {len(data.get('CVE', []))}"),
        html.P(f"Total CVE Score: {round(sum(data.get('CVE_NVD', {}).values()), 1)}"),
        html.P(f"Critical Functions: {', '.join(data.get('critical_functions', [])) or 'None'}"),
        html.P(f"Privilege: {data.get('privilege', 'N/A')}"),
        html.P(f"Rack: {data.get('rack_name', 'N/A')}")
    ])