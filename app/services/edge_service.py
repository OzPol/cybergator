from app.services.data_loader import get_nodes, save_nodes_data

def add_edge(source_node_id, target_node_id):
    nodes = get_nodes()
    for node in nodes:
        if node["node_id"] == source_node_id:
            if "connected_to" not in node:
                node["connected_to"] = []
            if target_node_id not in node["connected_to"]:
                node["connected_to"].append(target_node_id)
    save_nodes_data(nodes)

def remove_edge(source_node_id, target_node_id):
    nodes = get_nodes()
    edge_removed = False

    for node in nodes:
        if node["node_id"] == source_node_id and "connected_to" in node:
            if target_node_id in node["connected_to"]:
                node["connected_to"].remove(target_node_id)
                edge_removed = True

        if node["node_id"] == target_node_id and "connected_to" in node:
            if source_node_id in node["connected_to"]:
                node["connected_to"].remove(source_node_id)
                edge_removed = True

    if edge_removed:
        save_nodes_data(nodes)
    else:
        raise ValueError(f"Edge between '{source_node_id}' and '{target_node_id}' not found.")

