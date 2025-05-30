import json
import os
import shutil  # For backup reset
import pandas as pd

# Path to JSON files
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/json/")
BACKUP_PATH = os.path.join(DATA_PATH, "../data/backup/")
CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/csv/")

def load_json(filename):
    """Loads a JSON file from the data/json/ directory."""
    with open(os.path.join(DATA_PATH, filename), "r") as f:
        return json.load(f)

def load_xlsx(filename):
    """Loads an XLSX file and returns a list of dictionaries."""
    filepath = os.path.join(CSV_PATH, filename)
    df = pd.read_csv(filepath)  # Load the CSV file into a DataFrame
    return df.to_dict(orient="records")  # Convert DataFrame to a list of dictionaries

# Functions to get specific data
def get_nodes():
    return load_json("Nodes_Complete.json")

def get_risk_factors():
    return load_json("Risk_Factors.json")

def get_attack_tree():
    return load_json("Attack_Tree.json")

def get_critical_functions():
    return load_json("Critical_Functions.json")

def get_fuzzy_set():
    return load_json("Fuzzy_Set.json")

def get_software_inventory():
    return load_xlsx("software_inventory.csv")

def get_all_nodes():
    # Returns node names and IDs formatted for Dash dropdowns.
    nodes_data = get_nodes()
    return [{"label": node["node_name"], "value": node["node_id"]} for node in nodes_data]

def get_all_software():
    # Load software inventory from CSV and return as a DataFrame.
    filepath = os.path.join(CSV_PATH, "software_inventory.csv")
    df = pd.read_csv(filepath)
    
# Return software grouped by Make → Versions for dropdowns.
    # Remove duplicates to get unique software entries
    unique_software = df[['software_make', 'software_description', 'software_version', 'software_id']].drop_duplicates()

    # Group by software_make
    software_options = {}
    for _, row in unique_software.iterrows():
        make = row["software_make"]
        # version_label = f"{row['software_description']} ({row['software_version']})"
        version_label = f"{row['software_version']}"
        version_value = row["software_id"]

        if make not in software_options:
            software_options[make] = []

        software_options[make].append({"label": version_label, "value": version_value})

    return software_options

def save_nodes_data(updated_nodes):
    # Saves updated node data back to Nodes_Complete.json.
    try:
        with open(os.path.join(DATA_PATH, "Nodes_Complete.json"), "w") as f:
            json.dump(updated_nodes, f, indent=4)
    except Exception as e:
        print(f"Error saving nodes data: {e}")  # Debugging output

def reset_nodes_data():
    # Resets `Nodes_Complete.json` from backup.
    try:
        shutil.copy(os.path.join(BACKUP_PATH, "Nodes_Complete.json"), os.path.join(DATA_PATH, "Nodes_Complete.json"))
        print("Nodes reset to backup.")
    except Exception as e:
        print(f"Error restoring backup: {e}")
        

def save_json(data, filename):
    # Saves data to a JSON file in the data/json/ directory.
    try:
        filepath = os.path.join(DATA_PATH, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {filename}: {e}")  # Debugging output

def get_software_cves():
    # Loads the software_cves.json file.
    filepath = os.path.join(DATA_PATH, "software_cves.json")
    if not os.path.exists(filepath):
        return {}
    
    with open(filepath, "r") as f:
        return json.load(f)

def get_next_software_id():
    # Generate the next available software ID.
    software_cves = get_software_cves()

    if not software_cves:
        return "SW001"

    existing_ids = sorted(int(k[2:]) for k in software_cves.keys() if k.startswith("SW"))
    next_id = f"SW{existing_ids[-1] + 1:03d}"  # Format as "SWXXX"
    return next_id

def get_node_types():
    nodes = get_nodes()
    return sorted(set(node.get("node_type", "Unknown") for node in nodes))

def get_software_dropdown_options_OLD():
    df = pd.read_csv(os.path.join(CSV_PATH, "software_inventory.csv"))
    df = df[['software_make', 'software_version']].drop_duplicates()

    software_dict = {}
    for _, row in df.iterrows():
        make = row["software_make"]
        version = row["software_version"]

        if make not in software_dict:
            software_dict[make] = []

        software_dict[make].append({"label": version, "value": version})

    make_options = [{"label": make, "value": make} for make in software_dict]
    return make_options, software_dict

def get_software_dropdown_options():
    df = pd.read_csv(os.path.join(CSV_PATH, "software_inventory.csv"))
    df = df[['software_make', 'software_version']].drop_duplicates()

    software_dict = {}
    for _, row in df.iterrows():
        make = row["software_make"]
        version = row["software_version"]

        if make not in software_dict:
            software_dict[make] = []

        software_dict[make].append({"label": version, "value": version})

    make_options = [{"label": make, "value": make} for make in software_dict]
    return make_options, software_dict

def get_software_metadata(make, version):
    """Returns software_id, description, and other details from software_cves.json"""
    data = get_software_cves()
    for sid, entry in data.items():
        if entry["make"] == make and entry["version"] == version:
            return {
                "software_id": sid,
                "description": entry["description"],
                "cves": entry.get("cves", {}),
                "make": make,
                "version": version
            }
    raise ValueError(f"No software match found for {make} {version}")


def append_software_entry_OLD(node_id, software_id, software_version):
    filepath = os.path.join(CSV_PATH, "software_inventory.csv")
    df = pd.read_csv(filepath)

    if node_id in df["node_id"].values:
        return

    match = df[(df["software_id"] == software_id) & (df["software_version"] == software_version)]
    if match.empty:
        return

    row = match.iloc[0]
    new_entry = {
        "rack": row["rack"],
        "rack_group": row["rack_group"],
        "node_id": node_id,
        "node_name": f"Linked_{node_id}",
        "critical": row["critical"],
        "software_id": row["software_id"],
        "software_make": row["software_make"],
        "software_description": row["software_description"],
        "software_version": row["software_version"]
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(filepath, index=False)
    
def append_software_entry(node_id, node_name, software_id, software_make,
                        software_description, software_version, rack_name, category):
    filepath = os.path.join(CSV_PATH, "software_inventory.csv")
    df = pd.read_csv(filepath)

    # Prevent duplicate entry for same node + software
    if ((df["node_id"] == node_id) & (df["software_id"] == software_id)).any():
        return

    new_entry = {
        "category": category,
        "rack_name": rack_name,
        "node_id": node_id,
        "node_name": node_name,
        "is_in_use": True,
        "software_id": software_id,
        "software_make": software_make,
        "software_description": software_description,
        "software_version": software_version
    }

    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(filepath, index=False)


def get_critical_function_keys():
    data = get_critical_functions()
    return [item["Function_Number"] for item in data.get("System_Critical_Functions", [])]

def get_rack_list():
    path = os.path.join(DATA_PATH, "racks.json")
    with open(path, "r") as f:
        return json.load(f)["racks"]

def get_rack_options():
    return [{"label": r, "value": r} for r in get_rack_list()]

def add_node_to_software_cves(software_id, node_id):
    """Adds a node ID to the specified software's 'nodes' list in software_cves.json."""
    filepath = os.path.join(DATA_PATH, "software_cves.json")

    # Load the existing software CVEs data
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to read software_cves.json: {e}")

    if software_id not in data:
        raise ValueError(f"Software ID '{software_id}' not found in software_cves.json")

    # Ensure 'nodes' key exists and append if not already present
    nodes_list = data[software_id].setdefault("nodes", [])
    if node_id not in nodes_list:
        nodes_list.append(node_id)

    # Save updated data back to file
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise RuntimeError(f"Failed to write to software_cves.json: {e}")

def remove_node_from_software_inventory(node_id):
    filepath = os.path.join(CSV_PATH, "software_inventory.csv")
    try:
        df = pd.read_csv(filepath)
        df = df[df["node_id"] != node_id]
        df.to_csv(filepath, index=False)
        print(f"Removed node '{node_id}' from software_inventory.csv")
    except Exception as e:
        print(f"Error removing node from software_inventory.csv: {e}")


def remove_node_from_software_cves(node_id):
    """Removes a node from all software entries in software_cves.json."""
    try:
        data = get_software_cves()
        modified = False
        for sw in data.values():
            if "nodes" in sw and node_id in sw["nodes"]:
                sw["nodes"].remove(node_id)
                modified = True

        if modified:
            save_json(data, "software_cves.json")
            print(f"Removed node '{node_id}' from software_cves.json")
    except Exception as e:
        print(f"Error updating software_cves.json: {e}")
