import os
import json
import networkx as nx
from pyvis.network import Network
from app.services.data_loader import get_nodes
from dash import html, dcc
import dash_bootstrap_components as dbc
# Paths
ATTACK_TREE_PATH = "app/data/json/Attack_Tree.json"
TEMP_HTML_LOGIC = "assets/attack_tree_logical.html"
TEMP_HTML_MAPPING = "assets/attack_tree_system_mapping.html"

def generate_logical_attack_tree():
    """Generates logical attack tree: Goal → Step → Critical Function."""
    with open(ATTACK_TREE_PATH, "r") as f:
        attack_tree = json.load(f)

    G = nx.DiGraph()
    color_map = {
        "goal": "red",
        "step": "orange",
        "critical_function": "blue"
    }

    for goal in attack_tree["attack_goals"]:
        goal_id = goal["goal_id"]
        goal_name = goal["goal_name"]
        G.add_node(goal_id, label=goal_name, color=color_map["goal"], size=22,
                    title=f"Attack Goal: {goal_name} ({goal_id})")

        for step in goal["steps"]:
            step_id = step["step_id"]
            cve = step.get("cve", "N/A")
            step_label = f"{step['name']}\n({cve})"
            tooltip = (
                f"Step: {step['name']}\n"
                f"CVE: {cve}\n"
                f"Tactic: {step['tactic']}\n"
                f"Technique: {step['technique']}\n"
                f"Probability: {step['probability']}"
            )

            G.add_node(step_id, label=step_label, color=color_map["step"], size=20, title=tooltip)
            if not G.has_edge(goal_id, step_id):
                G.add_edge(goal_id, step_id, color="gray")

            for func in step["critical_functions_impacted"]:
                func_label = f"CF {func}"
                if not G.has_node(func):
                    G.add_node(func, label=func_label, color=color_map["critical_function"], size=30,
                                title=f"Critical Function ID: {func}")
                if not G.has_edge(step_id, func):
                    G.add_edge(step_id, func, color="blue")

    net = Network(height="1600px", width="100%", directed=True, bgcolor="#222222", font_color="white")
    net.barnes_hut(gravity=-2000, central_gravity=0.2, spring_length=200, spring_strength=0.05)
    net.toggle_physics(True)       

    for nid, data in G.nodes(data=True):
        net.add_node(nid, **data)
    for src, tgt, edata in G.edges(data=True):
        net.add_edge(src, tgt, color=edata.get("color", "gray"))

    # os.makedirs("assets", exist_ok=True)
    net.write_html(TEMP_HTML_LOGIC, notebook=False, open_browser=False)


def generate_critical_function_mapping():
    """Generates mapping: Critical Function → System Node."""
    with open(ATTACK_TREE_PATH, "r") as f:
        attack_tree = json.load(f)
    nodes_data = get_nodes()

    G = nx.DiGraph()
    color_map = {
        "critical_function": "blue",
        "system_node": "lightblue"
    }

    impacted_functions = set()
    for goal in attack_tree["attack_goals"]:
        for step in goal["steps"]:
            impacted_functions.update(step["critical_functions_impacted"])

    for func in impacted_functions:
        func_label = f"CF {func}"
        G.add_node(func, label=func_label, color=color_map["critical_function"], size=30,
                    title=f"Critical Function: {func}")

    for node in nodes_data:
        for func in node.get("critical_functions", []):
            if func in impacted_functions:
                node_id = node["node_id"]
                label = node["node_name"]
                cves = ", ".join(node.get("CVE", []))
                score = round(sum(node.get("CVE_NVD", {}).values()), 2)
                tooltip = (
                    f"System Node: {label}\n"
                    f"Node Type: {node.get('node_type')}\n"
                    f"CVEs: {cves}\n"
                    f"Total Score: {score}"
                )
                G.add_node(node_id, label=label, color=color_map["system_node"], size=20, title=tooltip)
                G.add_edge(func, node_id, color="green")

    net = Network(height="1600px", width="100%", directed=True, bgcolor="#222222", font_color="white")
    net.barnes_hut(gravity=-2000, central_gravity=0.2, spring_length=200, spring_strength=0.05)
    net.toggle_physics(True)

    for nid, data in G.nodes(data=True):
        net.add_node(nid, **data)
    for src, tgt, edata in G.edges(data=True):
        net.add_edge(src, tgt, color=edata.get("color", "gray"))

    # os.makedirs("assets", exist_ok=True)
    net.write_html(TEMP_HTML_MAPPING, notebook=False, open_browser=False)



def attack_tree_layout():
    from app.views.pages.attack_tree import (
        generate_logical_attack_tree,
        generate_critical_function_mapping
    )
    generate_logical_attack_tree()
    generate_critical_function_mapping()

    return html.Div([
        html.H3("Attack Tree Visualization"),

        dcc.Tabs([
            dcc.Tab(label="Logical Attack Tree", children=[
                html.Iframe(
                    src="/assets/attack_tree_logical.html",
                    style={"width": "100%", "height": "1600px", "border": "2px solid #ccc"}
                )
            ]),
            dcc.Tab(label="System Mapping (CF → Nodes)", children=[
                html.Iframe(
                    src="/assets/attack_tree_system_mapping.html",
                    style={"width": "100%", "height": "1600px", "border": "2px solid #ccc"}
                )
            ])
        ])
    ])
