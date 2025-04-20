import json
import os
# PRIVILEGES_PATH = "app/data/json/privileges.json"

# === Load Static Data ===
RACKS_PATH = os.path.join( "app", "data", "json", "racks.json")
NODES_PATH = os.path.join("app", "data", "json", "Nodes_Complete.json")

with open(NODES_PATH, "r") as f:
    NODES_DATA = json.load(f)
    
with open(RACKS_PATH, "r") as f:
    RACK_LIST = json.load(f).get("racks", [])

# === NodeType → Privilege Role Mapping ===
NODETYPE_TO_PRIVILEGE = {
    "SAN": "SA",
    "SAN Archive": "SA",
    "SAN Archive Backup": "SA",
    "Server": "IT",
    "Workstation": "EP",
    "Switch": "INFRA",
    "Router": "INFRA",
    "Firewall": "INFRA"
}
def build_privilege_lookup_from_type():
    """Returns {node_id: privilege_role} based on exact node_type (no lowercasing)."""
    result = {}
    for node in NODES_DATA:
        node_id = node["node_id"]
        node_type = node.get("node_type", "")
        role = NODETYPE_TO_PRIVILEGE.get(node_type, "GENERAL")
        result[node_id] = role
    return result

# === Rack-Based Constraint ===
def can_traverse_rack_boundary(src_node, tgt_node, cve_meta):
    if src_node.get("rack_name") == tgt_node.get("rack_name"):
        return True
    av = cve_meta.get("attack_vector", "")
    return av == "NETWORK"

# === Privilege Constraint ===
PRIVILEGE_LOOKUP = build_privilege_lookup_from_type()
def has_access_to_node(attacker_priv, target_node_id):
    required_priv = PRIVILEGE_LOOKUP.get(target_node_id)
    if required_priv is None:
        return True  # No restriction defined
    return attacker_priv == required_priv

# === Shared Vulnerable Software ===
def nodes_share_vulnerable_software(node1, node2, software_inventory):
    s1 = set(node1.get("software_ids", []))
    s2 = set(node2.get("software_ids", []))
    shared = s1.intersection(s2)
    return len(shared) > 0

# === Redundancy Evaluation ===
def is_redundant_and_resilient(new_node, ref_node):
    same_func = set(new_node.get("critical_functions", [])) == set(ref_node.get("critical_functions", []))
    same_or_lower_crit = new_node.get("resilience_penalty", 1.0) <= ref_node.get("resilience_penalty", 1.0)
    same_or_lower_cve = sum(new_node.get("CVE_NVD", {}).values()) <= sum(ref_node.get("CVE_NVD", {}).values())
    return same_func and same_or_lower_crit and same_or_lower_cve

# === Entry Point Eligibility ===
def is_valid_entry_node(node, cve_id, cve_meta):
    if cve_id not in node.get("CVE", []):
        return False
    av = cve_meta.get("attack_vector", "")
    pr = cve_meta.get("privileges_required", "")
    ui = cve_meta.get("user_interaction", "")
    return av in {"NETWORK", "ADJACENT_NETWORK", "LOCAL"} and pr in {"NONE", "LOW", "NA"} and ui in {"NONE", "NA"}

"""
constraints.py

This module defines formally grounded, justifiable constraints used to govern
attack propagation and system traversal within the CyberGator simulation framework.

These constraints support the design-based resilience assessment of cyber-physical systems
where live telemetry is unavailable, and all inference must be based on system topology,
vulnerability mapping (CVE/NVD), functional roles, privilege levels, and logical segmentation
(as derived from SUE2 documentation and structured data files).

The goal is to enforce realistic simulation logic while avoiding fake or hypothetical logic
(e.g., simulated privilege escalation or fabricated zero-day exploits). All constraints are
derived from or supported by available system documentation.


    Let G = (V, E) be the Graph representing the CPS
    V = Set of system nodes (e.g., servers, firewalls, workstations).
    E = Set of edges representing logical or physical dependencies between nodes.

    Node Attributes:
    Vulnerability Score V(v): Represents node-specific risk based on CVE scores from the National Vulnerability Database (NVD).
    Criticality Weight C(v): Defines the functional importance of the node based on its assigned critical functions.
    Centrality Metrics X(v): Measures the structural importance of nodes using:
    Betweenness Centrality (influence in shortest paths).
    Degree Centrality (connectivity to other nodes).
    Closeness Centrality (proximity to all other nodes).
    Eigenvector Centrality (influence based on neighbors' importance).
    Redundancy Indicator Rd(v): Determines whether a node has backup systems.
    Switch Dependency S(v): Identifies nodes reliant on networking switches.
    Environmental Risk E(v, t): Accounts for external risks (e.g., natural disasters, physical security vulnerabilities) using fuzzy logic analysis.
    Edge Attributes:
    Connectivity Strength W(u, v): Measures the reliability of the connection between two nodes.
    Attack Probability P(u, v): Represents the likelihood of an attack propagating from node u to node v.


Constraint Categories Implemented:
    Node attributes including rack_name, CVE, CVE_NVD, connected_to, critical_functions, software
    A known mapping of racks, critical nodes, and system roles from the SUE2 documentation
    Attack transition conditions based on real CVSS metadata (AV, PR, UI)
    
1. Rack Segmentation Constraint:
    - Compares rack_name between two nodes
    - Allows same-rack propagation unconditionally
    - Allows cross-rack propagation only under valid CVE + privilege
    - Restricts lateral movement between physical or logical zones (racks).
    - Cross-rack propagation is allowed only under specific conditions (e.g., attack vector = NETWORK).
    - This is based on the assumption that nodes in different racks are logically or physically isolated.
    
        Let rack(v) be the rack of node v.
            Allow traversal between node u → v iff:
            rack(u) == rack(v)
            OR
            AV(cve) == "NETWORK"  # CVE attack vector justifies remote traversal

            Alternative:
            Use a lookup of allowed inter-rack flows (e.g., from Firewall to Server), and block anything not explicitly whitelisted.

    Partition V into disjoint sets {V₁, V₂, ..., Vₖ} (racks). Then:
        ∀(u,v) ∈ E: if rack(u) ≠ rack(v), allow traversal only if:
        AV=NETWORK or
        has_privileged_access(u) is true

2. Privilege-Based Access Control:
    - Each node is assigned a required privilege level.
    - Attackers may only access nodes that require privileges less than or equal to their current level.
    - Privileges are mapped explicitly using a structured privilege matrix

    PRIVILEGE MODELING WITH RBAC
    SUE2 defines 4 roles with varying privileges
    - SA (root to all systems, including SAN/Archive)
    - EP, TE, CMgmt have owner access to domains tied to their workflows (Eng, Test, Mgmt)

    Example: 
    # If a node is an SA machine, an attacker gaining access can control all storage, VM, and audit logs.
    if role == "SA":
        reachable.add("SAN")
        reachable.add("Archive")



3. CVE-Aware Entry Point Filtering:
    - Defines valid entry nodes based on CVE properties (AV, PR, UI).
    - Avoids invalid attack assumptions, while allowing known and realistic exploitation paths.
    

4. Redundancy Validation:
    - Additional nodes are only considered resilience-enhancing if:
    a. They perform the same critical function.
    b. They have equal or lower vulnerability and criticality.
    c. They do not expose additional privilege risks.
        CRS(G') ≥ CRS(G) iff the added node satisfies:
            F(new_node) ∈ F(original_node)           # same function
            C(new_node) ≤ C(original_node)           # equal or lower criticality
            V(new_node) ≤ V(original_node)           # equal or lower vulnerability
            priv(new_node) ≤ priv(original_node)     # no new privilege exposure
        where:
            CRS(G) = Criticality Risk Score of the original graph
            CRS(G') = Criticality Risk Score of the modified graph
            F(v) = set of critical functions served by node v
            C(v) = criticality weight
            V(v) = max or sum of CVE scores
            priv(v) = required privilege level

5. Shared Vulnerable Software:
    - Finds nodes that share at least one vulnerable software package
    - Nodes that share vulnerable software may form valid lateral propagation paths.
    - Supports modeling of zero-day-like behavior without fabricating CVEs.
    
        If node_u and node_v share a software s and:
            - s is vulnerable (CVE exists)
            - s is installed on both nodes
            - s is not patched on either node
        Then node_u and node_v are connected in the attack graph.
        
            CVE_NVD(s) >= threshold
            AND s is not patched
                → Add attack edge (u, v)
        This allows for lateral movement between nodes that share vulnerable software.

6. Monotonic Resilience Constraint
    Resilience score must increase when:
        - Vulnerability is removed (CVE patched)


All constraint functions are designed to be modular, explainable, and reusable across
simulation components including attack graph generation, reachability modeling, and
resilience score computation.
"""


