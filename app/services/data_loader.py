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