"""Restore the existing sample backups without changing the scoring model."""
from copy import deepcopy
import json
from pathlib import Path
import sys

import networkx as nx

from app.services import data_loader


JSON_BACKUPS = (
    "Nodes_Complete.json", "software_cves.json", "Attack_Tree.json",
    "Critical_Functions.json", "Risk_Factors.json", "Fuzzy_Set.json",
)
CSV_BACKUPS = ("software_inventory.csv", "hardware_inventory_nodes.xlsx")


def reset_all_data():
    """Restore backed-up inputs, regenerate metrics, and refresh loaded caches."""
    data_path = Path(data_loader.DATA_PATH)
    backup_path = Path(data_loader.BACKUP_PATH)
    csv_path = Path(data_loader.CSV_PATH)

    # Read every backup before changing live data. A missing or invalid backup
    # must fail visibly instead of reporting a reset or restoring only some files.
    copies = [(data_path / name, (backup_path / name).read_bytes()) for name in JSON_BACKUPS]
    copies += [(csv_path / name, (backup_path / name).read_bytes()) for name in CSV_BACKUPS]
    restored = {name: json.loads(content) for name, (_, content) in zip(JSON_BACKUPS, copies)}
    for destination, content in copies:
        destination.write_bytes(content)

    from app.services import resilience_score_calculator as calculator

    nodes = restored["Nodes_Complete.json"]
    fuzzy_scores = calculator.calculate_all_work_areas_risk_fuzzy(
        data_path / "Risk_Factors.json", data_path / "Fuzzy_Set.json"
    )
    graph = nx.Graph()
    for node in nodes:
        graph.add_node(node["node_id"])
        for neighbor in node.get("connected_to", []):
            graph.add_edge(node["node_id"], neighbor)
    scores = calculator.calculate_resilience_scores(
        nodes, graph, fuzzy_scores, calculator.critical_function_weights
    )
    system_score = calculator.calculate_system_resilience(scores)
    output_path = data_path / "output"
    output_path.mkdir(exist_ok=True)
    (output_path / "Resilience_Scores.json").write_text(json.dumps(scores, indent=4))
    calculator.save_resilience_scores_to_file(
        scores, system_score, output_path / "System_Resilience_Scores.json"
    )
    calculator.calculate_and_save_individual_metrics(
        nodes, graph, fuzzy_scores, calculator.critical_function_weights,
        output_path / "Individual_Node_Metrics.json",
    )

    # These prototype modules cache sample inputs at import time. Restore those
    # caches too, including when the server started with an already edited volume.
    calculator.nodes_data = deepcopy(nodes)
    calculator.risk_factors_data = restored["Risk_Factors.json"]
    calculator.fuzzy_sets = restored["Fuzzy_Set.json"]
    calculator.environmental_risk_scores_fuzzy = fuzzy_scores
    calculator.G = graph
    calculator.resilience_scores = scores
    calculator.system_resilience_score = system_score
    constraints = sys.modules.get("app.services.constraints")
    if constraints is not None:
        constraints.NODES_DATA = deepcopy(nodes)
        constraints.PRIVILEGE_LOOKUP = constraints.build_privilege_lookup_from_type()
    simulation = sys.modules.get("app.views.pages.apt_simulation")
    if simulation is not None:
        simulation.NODES_DATA = deepcopy(nodes)
        simulation.PRIVILEGE_LOOKUP = simulation.build_privilege_lookup_from_type()
    fsm = sys.modules.get("app.services.fsm_simulation")
    if fsm is not None:
        fsm.nodes_data = deepcopy(nodes)
        fsm.fuzzy_scores = fuzzy_scores

    return {"node_count": len(nodes), "system_resilience_score": system_score}
