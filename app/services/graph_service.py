import json
from app.services.data_loader import get_nodes, save_nodes_data

def load_graph_data():
    """Load nodes and edges from JSON file"""
    try:
        with open("app/data/json/Nodes_Complete.json", "r") as f:
            data = json.load(f)

        nodes = [{"id": str(node["node_id"]), "label": node["node_name"]} for node in data]
        edges = []
        for node in data:
            if "connected_to" in node:
                for target_id in node["connected_to"]:
                    edges.append({"source": str(node["node_id"]), "target": str(target_id)})

        return {"nodes": nodes, "edges": edges}
    except Exception as e:
        return {"error": str(e)}

def add_node_to_system_graph(node_data, software_id=None, software_cves=None):
    nodes = get_nodes() 
    if software_id and software_cves:
        node_data["CVE"] = software_cves.get(software_id, [])
        node_data["CVE_NVD"] = {}
    else:
        node_data["CVE"] = []
        node_data["CVE_NVD"] = {}

    nodes.append(node_data)
    save_nodes_data(nodes)