# BN
import os
import json
import datetime
import networkx as nx

from app.services.resilience_score_calculator import (
    calculate_resilience_scores,
    calculate_all_work_areas_risk_fuzzy
)

# ================================
# Data Load (moved OUT of function)
# ================================
DATA_DIR = os.path.join("app", "data", "json")
nodes_path = os.path.join(DATA_DIR, "Nodes_Complete.json")
fuzzy_path = os.path.join(DATA_DIR, "Fuzzy_Set.json")
risk_factors_path = os.path.join(DATA_DIR, "Risk_Factors.json")

with open(nodes_path, "r") as f:
    nodes_data = json.load(f)

fuzzy_scores = calculate_all_work_areas_risk_fuzzy(risk_factors_path, fuzzy_path)

def load_critical_functions():
    path = os.path.join("app", "data", "json", "Critical_Functions.json")
    with open(path, "r") as f:
        data = json.load(f)
    # Extract all structured fields
    functions = data.get("System_Critical_Functions", [])
    parsed = {}
    for func in functions:
        fn = func["Function_Number"]
        parsed[fn] = {
            "work_area": func.get("Work_Area"),
            "criticality": func.get("Criticality"),
            "weight": func.get("Criticality_Value", 1),
            "nodes": func.get("Nodes", [])
        }
    return parsed


def extract_criticality_weights(nodes_data):
    function_data = load_critical_functions()
    weights = {fn: details["weight"] for fn, details in function_data.items()}
    criticality_weights = {}
    for node in nodes_data:
        functions = node.get("critical_functions", [])
        score = sum(weights.get(f, 1) for f in functions)
        criticality_weights[node["node_id"]] = score
    return criticality_weights


# def extract_criticality_weights(nodes_data):
#    weights = {
#        "F01": 3, "F02": 3, "F03": 3, "F04": 2, "F05": 3, "F06": 3,
#        "F07": 2, "F08": 2, "F09": 2, "F10": 2, "F11": 1, "F12": 1,
#        "F13": 1, "F14": 1, "F15": 1, "F16": 3, "F18": 3
#    }
#    return {
#        node['node_id']: sum(weights.get(func, 1) for func in node.get('critical_functions', []))
#        for node in nodes_data
#    }

def extract_nvd_scores_from_nodes(nodes_data):
    nvd_scores = {}
    for node in nodes_data:
        for cve, score in node.get('CVE_NVD', {}).items():
            nvd_scores[cve] = score
    return nvd_scores

def build_graph_from_nodes(nodes_data):
    G = nx.Graph()
    for node in nodes_data:
        G.add_node(node['node_id'])
        for neighbor in node.get('connected_to', []):
            G.add_edge(node['node_id'], neighbor)
    return G


# ====================
# FSM Core Definitions
# ====================
class SystemState:
    def __init__(self, name, impact):
        self.name = name
        self.impact = impact

class FSM:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, state):
        self.states[state.name] = state

    def set_initial_state(self, state_name):
        self.current_state = self.states[state_name]

    def transition_to(self, state_name):
        if state_name in self.states:
            self.current_state = self.states[state_name]
            return self.current_state.impact
        return None

    def get_current_state_impact(self):
        return self.current_state.impact

    def apply_resilience_score(self, node_id, resilience_scores):
        return next((item['resilience_score'] for item in resilience_scores if item['node_id'] == node_id), 100)


def calculate_new_resilience(initial_resilience, fsm):
    penalty_scale = 0.2
    state_impact = fsm.get_current_state_impact()
    drop = penalty_scale * state_impact * initial_resilience
    return round(max(0, initial_resilience - drop), 5)


def simulate_fsm_with_resilience(nodes_data, cvss_scores, resilience_scores):
    fsm = FSM()
    fsm.add_state(SystemState("Normal", 1.0))
    fsm.add_state(SystemState("Recovery", 0.75))
    fsm.add_state(SystemState("Degraded", 0.5))
    fsm.add_state(SystemState("Under Attack", 0.2))
    fsm.add_state(SystemState("Failure", 0.1))
    fsm.set_initial_state("Normal")

    for node in nodes_data:
        node_id = node["node_id"]
        node_name = node["node_name"]

        initial = fsm.apply_resilience_score(node_id, resilience_scores)

        for cve in node.get("CVE", []):
            severity = cvss_scores.get(cve, 0)
            if severity >= 8.0:
                fsm.transition_to("Under Attack")
            elif 4.0 <= severity < 8.0:
                fsm.transition_to("Degraded")
            else:
                fsm.transition_to("Normal")

        updated = calculate_new_resilience(initial, fsm)

        for r in resilience_scores:
            if r['node_id'] == node_id:
                r['resilience_score'] = updated

        print(f"Node: {node_name} (ID: {node_id}), FSM State: {fsm.current_state.name}, "
            f"Initial: {initial}, Final: {updated}")


# ==========================
# Run FSM Simulation Wrapper
# ==========================
def run_fsm_simulation():
    criticality_weights = extract_criticality_weights(nodes_data)
    graph = build_graph_from_nodes(nodes_data)
    resilience_scores = calculate_resilience_scores(nodes_data, graph, fuzzy_scores, criticality_weights)
    nvd_scores = extract_nvd_scores_from_nodes(nodes_data)

    simulate_fsm_with_resilience(nodes_data, nvd_scores, resilience_scores)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = os.path.join("app", "sim_logs", f"fsm_sim_{timestamp}")
    os.makedirs(output_dir, exist_ok=True)

    out_path = os.path.join(output_dir, "Resilience_Scores_FSM.json")
    with open(out_path, "w") as f:
        json.dump(resilience_scores, f, indent=4)
    print(f"\nFSM simulation complete. Saved to: {out_path}")


if __name__ == "__main__":
    run_fsm_simulation()
