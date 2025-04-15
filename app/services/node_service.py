import json
from app.services.data_loader import (
    get_nodes,
    save_nodes_data,
    append_software_entry,
    add_node_to_software_cves,
    get_software_metadata,
    get_software_cves,
    save_json,
    remove_node_from_software_inventory
)

def add_node_to_system_graph(node_id, node_name, node_type, critical_functions,
                            connected_to, backup_role, data_redundancy, risk_factor,
                            switch_dependency, resilience_penalty,
                            software_make, software_version,
                            rack_name, category):

    # Get software metadata from software_cves.json
    software_meta = get_software_metadata(software_make, software_version)
    software_id = software_meta["software_id"]
    software_description = software_meta["description"]
    cves = list(software_meta["cves"].keys())
    cve_nvd = software_meta["cves"]

    # Build the new node dict
    new_node = {
        "node_id": node_id,
        "node_name": node_name,
        "node_type": node_type,
        "critical_functions": critical_functions,
        "connected_to": connected_to,
        "critical_data_stored": True if data_redundancy == "Yes" else False,
        "backup_role": None if backup_role == "null" else backup_role,
        "data_redundancy": data_redundancy,
        "redundancy": data_redundancy == "Yes",
        "risk_factor": risk_factor,
        "switch_dependency": switch_dependency,
        "resilience_penalty": float(resilience_penalty),
        "CVE": cves,
        "CVE_NVD": cve_nvd
    }

    # Load → Append → Save
    nodes = get_nodes()
    
    # Prevent duplicate node ID
    if any(n["node_id"] == node_id for n in nodes):
        raise ValueError(f"Node ID '{node_id}' already exists.")


    nodes.append(new_node)
    save_nodes_data(nodes)

    # Update software_inventory.csv
    append_software_entry(
        node_id=node_id,
        node_name=node_name,
        software_id=software_id,
        software_make=software_make,
        software_description=software_description,
        software_version=software_version,
        rack_name=rack_name,
        category=category
    )

    # Update software_cves.json → Add node ID under software
    add_node_to_software_cves(software_id, node_id)

    return new_node


def remove_node_from_system_graph(node_id):
    # Remove from Nodes_Complete.json
    nodes = get_nodes()
    updated_nodes = [n for n in nodes if n["node_id"] != node_id]

    if len(updated_nodes) == len(nodes):
        raise ValueError(f"Node '{node_id}' not found.")

    save_nodes_data(updated_nodes)

    # Remove from software_cves.json
    software_data = get_software_cves()
    for sw in software_data.values():
        if "nodes" in sw and node_id in sw["nodes"]:
            sw["nodes"].remove(node_id)
    save_json(software_data, "software_cves.json")

    # Remove from software_inventory.csv
    remove_node_from_software_inventory(node_id)

    return True
