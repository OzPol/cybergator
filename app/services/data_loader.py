import json
import os

# Path to JSON files
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/json/")

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
