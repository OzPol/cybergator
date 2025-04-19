import os
import json
import dash
from dash import html, dcc, Output, Input, State, callback, ctx
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

from dotenv import load_dotenv
load_dotenv()

# Load system data
with open("app/data/json/Nodes_Complete.json", "r") as f:
    NODES_DATA = json.load(f)

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
        node_id = node["node_id"]
        label = node["node_name"]
        node_type = node.get("node_type", "unknown").lower()
        functions = ", ".join(node.get("critical_functions", []))
        cve_count = len(node.get("CVE", []))
        cve_score_total = sum(node.get("CVE_NVD", {}).values())

        node_data = {
            "id": node_id,
            "label": f"{label}\nCVEs: {cve_count}",
            "node_type": node_type,
            "critical_functions": functions,
            "cve_count": cve_count,
            "cve_score": cve_score_total,
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

# Layout (Top Half of Page)
def simulation_apt_layout():
    return html.Div([
        dcc.Store(id="sim-system-graph-data"),
        dcc.Store(id="sim-hover-node-info"),

        html.H3("System Graph View", style={"marginTop": "20px"}),

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
                        # "label": "data(label)",
                        "background-color": "data(color)",
                        "width": 50,
                        "height": 50,
                        "text-valign": "center",
                        "text-halign": "center",
                        "font-size": 10,
                        "color": "#000"
                    },
                },
                {
                    "selector": "edge",
                    "style": {
                        "line-color": "#444",
                        "width": 2
                    },
                }
            ]
        ),
        html.Div(id="sim-node-hover-info", style={"marginTop": "20px"})
    ])


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
