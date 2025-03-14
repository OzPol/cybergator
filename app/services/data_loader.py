import json
import os
import shutil  # For backup reset

# Path to JSON files
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/json/")
BACKUP_PATH = os.path.join(DATA_PATH, "..data/json/backup/")

def load_json(filename):
    """Loads a JSON file from the data/json/ directory."""
    with open(os.path.join(DATA_PATH, filename), "r") as f:
        return json.load(f)

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

def save_nodes_data(updated_nodes):
    """Saves updated node data back to Nodes_Complete.json."""
    try:
        with open(os.path.join(DATA_PATH, "Nodes_Complete.json"), "w") as f:
            json.dump(updated_nodes, f, indent=4)
    except Exception as e:
        print(f"Error saving nodes data: {e}")  # Debugging output

def reset_nodes_data():
    """Resets `Nodes_Complete.json` from backup."""
    try:
        shutil.copy(os.path.join(BACKUP_PATH, "Nodes_Complete.json"), os.path.join(DATA_PATH, "Nodes_Complete.json"))
        print("Nodes reset to backup.")
    except Exception as e:
        print(f"Error restoring backup: {e}")