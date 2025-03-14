import json
import os
import networkx as nx

# ---------------------------------------------------------
# Overview:
# This code calculates resilience scores for nodes in a network based on multiple metrics:
# 1. Fuzzy Logic Calculation: For environmental risk factors.
# 2. Vulnerability Scores (CVE): Based on NVD CVE scores.
# 3. Centrality: How important a node is in the network.
# 4. Connectedness: How connected the node is to others.
# 5. Criticality: Importance based on associated critical functions.
# 6. Switch Dependency: Whether the node depends on switches for access.
# 7. Redundancy: Whether the node has redundancy built in (e.g., SAN backup).
# The final resilience score combines all these factors.
# See below the code for the step-by-step explanation of each metric.
# ---------------------------------------------------------

# Input files
# input_file = os.path.join("src", "maindata", "Risk_Factors.json")
# fuzzy_file = os.path.join("src", "maindata", "Fuzzy_Set.json")
# nodes_file = os.path.join("src", "maindata", "Nodes_Complete.json")

# Load nodes data
# with open(nodes_file, 'r') as file:
#    nodes_data = json.load(file)


DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/json/")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../data/json/output/")  # Directory for output files

input_file = os.path.join(DATA_PATH, "Risk_Factors.json")
fuzzy_file = os.path.join(DATA_PATH, "Fuzzy_Set.json")
nodes_file = os.path.join(DATA_PATH, "Nodes_Complete.json")

# output directory exists ?
os.makedirs(OUTPUT_PATH, exist_ok=True)

# LOAD ALL DATA AT ONCE
with open(nodes_file, 'r') as file:
    nodes_data = json.load(file)

with open(input_file, 'r') as file:
    risk_factors_data = json.load(file)

with open(fuzzy_file, 'r') as file:
    fuzzy_sets = json.load(file)

# Step 1: Define fuzzy logic for environmental risk
def calculate_fuzzy_membership(value, fuzzy_set):
    """
    Calculate the membership value for fuzzy logic based on fuzzy set.
    """
    left = fuzzy_set['left']
    peak = fuzzy_set['peak']
    right = fuzzy_set['right']

    if value == 'NA':  # Handle 'NA'
        return 0.0

    if left <= value <= peak:
        return (value - left) / (peak - left)  # Rising slope
    elif peak < value <= right:
        return (right - value) / (right - peak)  # Falling slope
    else:
        return 0.0

def calculate_environmental_risk_with_fuzzy_logic(work_area, fuzzy_sets):
    """
    Calculate the environmental risk for a given work area using fuzzy logic.
    """
    risk_factors = work_area['Risk_Factors']
    total_risk_score = 0
    for factor, value in risk_factors.items():
        if factor in fuzzy_sets and value in fuzzy_sets[factor]:
            fuzzy_set = fuzzy_sets[factor][value]
            membership_value = fuzzy_set['peak']
            total_risk_score += membership_value
    return total_risk_score

def calculate_all_work_areas_risk_fuzzy(input_file, fuzzy_file):
    """
    Calculate the environmental risk for all work areas using fuzzy logic.
    """
    with open(input_file, 'r') as file:
        work_area_data = json.load(file)
        
    with open(fuzzy_file, 'r') as fuzzy_file:
        fuzzy_sets = json.load(fuzzy_file)
        
    work_areas = work_area_data['work_areas']
    environmental_risk_scores_fuzzy = {}

    for area in work_areas:
        work_area_name = area['Work_Area']
        environmental_risk = calculate_environmental_risk_with_fuzzy_logic(area, fuzzy_sets)
        environmental_risk_scores_fuzzy[work_area_name] = round(environmental_risk, 1)

    return environmental_risk_scores_fuzzy

# FOR REFACTORING 
# environmental_risk_scores_fuzzy = calculate_all_work_areas_risk_fuzzy()

# Step 2: Calculate CVE vulnerability score for each node
def calculate_vulnerability_score(node):
    """
    Calculates the CVE vulnerability score for a node.
    """
    cve_scores = node.get('CVE_NVD', {})
    if cve_scores:
        # return sum(cve_scores.values()) / len(cve_scores)  # Average of all CVE scores
        # return max(cve_scores.values())  # Maximum CVE score
        return sum(cve_scores.values())
    return 0

# Step 3: Calculate centrality score for each node using NetworkX
def calculate_centrality_scores(graph):
    """
    Calculates the centrality score for each node using betweenness centrality.
    1. Betweenness Centrality: Measures how often a node is on the shortest paths between other nodes.
    2. Degree Centrality:  Measures the number of direct connections a node has
    3. Closeness Centrality: Measures how close a node is to all other nodes in the network.
    4. Eigenvector Centrality: Measures the influence of a node based on the influence of its neighbors.
    If eigenvector centrality fails to converge (which can happen in some graphs), we catch that error and set the centrality to 0 for all nodes.
    Finally, we average the four measures for each node and store that average in centrality_scores.
    """
    # return nx.betweenness_centrality(graph) # tried this first on its own but decided to expand to all centrality measures
    
    # Compute individual centrality measures
    betweenness = nx.betweenness_centrality(graph)
    degree = nx.degree_centrality(graph)
    closeness = nx.closeness_centrality(graph)
    
    try:
        eigenvector = nx.eigenvector_centrality(graph, max_iter=1000)
    except nx.PowerIterationFailedConvergence:
        eigenvector = {node: 0 for node in graph.nodes}

    # Average centrality across all four measures
    centrality_scores = {}
    for node in graph.nodes:
        centrality_scores[node] = (
            (betweenness.get(node, 0) + degree.get(node, 0) +
            closeness.get(node, 0) + eigenvector.get(node, 0)) / 4
        )
    
    return centrality_scores

# Step 4: Calculate connectedness score (number of edges) for each node
def calculate_connectedness_scores(graph):
    """
    Calculate connectedness score for each node based on the number of edges (degree).
    """
    return dict(graph.degree())

# Step 5: Calculate switch dependency score
def calculate_switch_dependency(node):
    """
    Returns the switch dependency weight for a node.
    """
    return node.get('switch_dependency_weight', 1.0)

# Step 6: Calculate redundancy score for each node
def calculate_redundancy(node):
    """
    Checks if the node has redundancy (e.g., backup or SAN redundancy).
    Nodes_Complete.json should have a 'redundancy' key for this.
    """
    if node.get('redundancy', False):
        return 0.8  # Lower penalty for redundancy
    return 1.0  # Full penalty if no redundancy

# Step 7: Calculate criticality of the node based on associated critical functions
def calculate_criticality(node, critical_function_weights):
    """
    Calculate the criticality score for a node based on the sum of its critical function weights.
    """
    critical_functions = node.get('critical_functions', [])
    return sum(critical_function_weights.get(func, 1) for func in critical_functions)

# Step 8: Map critical functions to work areas
critical_function_to_work_area = {
    "F01": "Engineering_Production",
    "F02": "EngineeringProduction",
    "F03": "Engineering_Production",
    "F04": "Test_Engineering",
    "F05": "IT_Cybersecurity",
    "F06": "IT_Cybersecurity",
    "F07": "Engineering_Production",
    "F08": "Test_Engineering",
    "F09": "Test_Engineering",
    "F10": "Company_Management",
    "F11": "Engineering_Production",
    "F12": "Test_Engineering",
    "F13": "Company_Management",
    "F14": "Company_Management",
    "F15": "Company_Management",
    "F16": "IT_Cybersecurity", 
    "F18": "IT_Cybersecurity"
}

# Step 9: Calculate the environmental risk for each node based on work areas
def calculate_node_environmental_risk(node, fuzzy_scores, critical_function_to_work_area):
    """
    Calculate the environmental risk for a node based on its associated critical functions
    and the corresponding work areas' risk factors.
    """
    critical_functions = node.get('critical_functions', [])
    total_risk_score = 0
    
    # Sum the environmental risk scores for all work areas corresponding to critical functions
    for func in critical_functions:
        work_area = critical_function_to_work_area.get(func)
        if work_area in fuzzy_scores:
            total_risk_score += fuzzy_scores[work_area]
    
    return total_risk_score


# Step 10: Final resilience score calculation
def calculate_resilience_scores(nodes_data, graph, fuzzy_scores, critical_function_weights):
    """
    Calculates resilience scores for all nodes by combining the fuzzy environmental risk score,
    CVE vulnerability, centrality, connectedness, switch dependency, and redundancy.
    
    Calculate resilience scores for all nodes by reducing a starting score of 100
    based on penalties for CVE scores, centrality, connectedness, etc., and then
    applying environmental risk penalties at the end.
    """
    # Start with a base score of 100 for each node
    base_score = 100

    # Pre-calculate graph metrics
    centrality_scores = calculate_centrality_scores(graph)
    connectedness_scores = calculate_connectedness_scores(graph)

    resilience_scores = []

    for node in nodes_data:
        node_id = node['node_id']
        resilience_score = base_score

        # Apply penalties (deduct from 100)
        cve_score = calculate_vulnerability_score(node)
        centrality = centrality_scores.get(node_id, 0)
        connectedness = connectedness_scores.get(node_id, 0)
        switch_dep = calculate_switch_dependency(node)
        redundancy = calculate_redundancy(node)
        criticality = calculate_criticality(node, critical_function_weights)
        
        # Deduct points for each factor
        resilience_score -= cve_score * 0.4  # CVE score penalty (weighted)
        resilience_score -= centrality * 0.2  # Centrality penalty (weighted)
        resilience_score -= connectedness * 0.2  # Connectedness penalty (weighted)
        resilience_score -= switch_dep * 0.2  # Switch dependency penalty
        resilience_score -= criticality * 0.3  # Criticality penalty
        resilience_score += redundancy * 0.2  # Redundancy reduces penalty

        # Calculate environmental risk for this node
        environmental_risk = calculate_node_environmental_risk(node, fuzzy_scores, critical_function_to_work_area)

        # Final adjustment: Divide resilience score by environmental risk (1 + risk factor)
        resilience_score /= (1 + environmental_risk)

        # check to make sure the resilience score doesn't drop below 0
        resilience_score = max(resilience_score, 0.001)

        # Store the calculated resilience score
        resilience_scores.append({
            'node_id': node_id,
            'node_name': node['node_name'],
            'resilience_score': round(resilience_score, 5),
        })

    return resilience_scores

# ---------------------------------------------------------

# Critical function weights
critical_function_weights = {"F01": 3, "F02": 3, "F03": 3, "F04": 2, "F05": 3,
                            "F06": 3, "F07": 2, "F08": 2, "F09": 2, "F10": 2,
                            "F11": 1, "F12": 1, "F13": 1, "F14": 1, "F15": 1, 
                            "F16": 3, "F18": 3}

# Load fuzzy environmental risk scores
environmental_risk_scores_fuzzy = calculate_all_work_areas_risk_fuzzy(input_file, fuzzy_file)

# Create graph from node connections
G = nx.Graph()
for node in nodes_data:
    G.add_node(node['node_id'])
    for connected_node in node['connected_to']:
        G.add_edge(node['node_id'], connected_node)

# Calculate resilience scores
resilience_scores = calculate_resilience_scores(nodes_data, G, environmental_risk_scores_fuzzy, critical_function_weights)

# Output the resilience scores
for score in resilience_scores:
    print(f"Node: {score['node_name']}, Resilience Score: {score['resilience_score']}")

# Save the resilience scores to a file
output_file_path = os.path.join(OUTPUT_PATH, "Resilience_Scores.json")
with open(output_file_path, 'w') as outfile:
    json.dump(resilience_scores, outfile, indent=4)

# Step 1: Function to calculate system resilience score
def calculate_system_resilience(resilience_scores):
    """
    Calculate the overall system resilience score by summing up all node resilience scores.
    """
    total_resilience = sum(node['resilience_score'] for node in resilience_scores)
    
        # Normalization: Divide the total resilience by the total number of nodes
    total_number_of_nodes = len(resilience_scores)
    
    # Normalize the total system resilience score
    normalized_system_resilience = total_resilience / total_number_of_nodes
    
    return round(normalized_system_resilience, 5)

# Step 2: Function to save resilience scores (both individual and system scores)
def save_resilience_scores_to_file(resilience_scores, system_resilience_score, output_file):
    """
    Saves the individual node resilience scores and the overall system resilience score to a JSON file.
    """
    # Add system resilience score to the JSON
    output_data = {
        "system_resilience_score": system_resilience_score,
        "individual_node_scores": resilience_scores
    }
    
    # Write the data to the file
    with open(output_file, 'w') as outfile:
        json.dump(output_data, outfile, indent=4)
    
    print(f"System and individual resilience scores saved to {output_file} after running resilience_score_calculator.py.")

# Step 3: Function to calculate and save individual metrics
def calculate_and_save_individual_metrics(nodes_data, graph, fuzzy_scores, critical_function_weights, output_file):
    """
    Calculates individual metrics for each node (CVE score, centrality, connectedness, etc.)
    and saves the results to a JSON file.
    """
    # Pre-calculate graph metrics
    centrality_scores = calculate_centrality_scores(graph)
    connectedness_scores = calculate_connectedness_scores(graph)

    individual_metrics = []  # List to collect individual node metrics

    for node in nodes_data:
        node_id = node['node_id']

        # Calculate individual metrics
        cve_score = calculate_vulnerability_score(node)
        centrality = centrality_scores.get(node_id, 0)
        connectedness = connectedness_scores.get(node_id, 0)
        switch_dep = calculate_switch_dependency(node)
        redundancy = calculate_redundancy(node)
        criticality = calculate_criticality(node, critical_function_weights)
        environmental_risk = calculate_node_environmental_risk(node, fuzzy_scores, critical_function_to_work_area)

        # Store the individual metrics for this node
        individual_metrics.append({
            'node_id': node_id,
            'node_name': node['node_name'],
            'cve_score': round(cve_score, 5),
            'centrality': round(centrality, 5),
            'connectedness': round(connectedness, 5),
            'switch_dependency': round(switch_dep, 5),
            'redundancy': round(redundancy, 5),
            'criticality': round(criticality, 5),
            'environmental_risk': round(environmental_risk, 5)
        })

    # Write individual metrics to JSON file
    with open(output_file, 'w') as metrics_file:
        json.dump(individual_metrics, metrics_file, indent=4)

    print(f"Individual node metrics have been saved to {output_file}.")

# ---------------------------------------------------------
# Integration: Calculate the resilience scores and metrics, save them to files, and print everything

# Calculate the node resilience scores (replace with your function call)
resilience_scores = calculate_resilience_scores(nodes_data, G, environmental_risk_scores_fuzzy, critical_function_weights)

# Calculate and output the overall system resilience score
system_resilience_score = calculate_system_resilience(resilience_scores)

# Print individual node resilience scores and system resilience score to the console
print("=== Individual Node Resilience Scores ===")
for score in resilience_scores:
    print(f"Node: {score['node_name']}, Resilience Score: {score['resilience_score']}")

print(f"\nOverall System Resilience Score: {system_resilience_score}")

# Define the output file paths for saving results
# system_output_file = os.path.join("src", "maindata_copy", "System_Resilience_Scores.json")
# individual_metrics_output_file = os.path.join("src", "maindata_copy", "Individual_Node_Metrics.json")


# Define the output file paths for saving results
system_output_file = "app/data/json/output/System_Resilience_Scores.json"
individual_metrics_output_file = "app/data/json/output/Individual_Node_Metrics.json"

# Save resilience scores to file (both individual node scores and system score)
save_resilience_scores_to_file(resilience_scores, system_resilience_score, system_output_file)

# Calculate and save individual node metrics
calculate_and_save_individual_metrics(
    nodes_data,
    G,
    environmental_risk_scores_fuzzy,
    critical_function_weights,
    individual_metrics_output_file
)

# print(len(nodes_data))

"""
CyberGator Resilience Score Calculation

Overview:
This script calculates the resilience scores for various nodes in a networked system, 
factoring in several metrics related to vulnerabilities, network structure, redundancy, 
and environmental risks. The resilience score starts at 100 and is reduced based on penalties 
related to criticality, centrality, connectedness, and other factors. At the end, the score 
is divided by an environmental risk factor to reflect the impact of real-world conditions.

Key Concepts:
1. **Base Resilience Score**: 
    - All nodes start with a resilience score of 100.
    - The score is then reduced based on several penalty factors, such as vulnerabilities 
    (CVE scores), criticality of the node, and how central and connected it is to the network.

2. **Environmental Risk Adjustment**:
    - After penalties are applied, each node's resilience score is further adjusted by dividing 
    it by (1 + environmental risk factor), where the environmental risk is derived from fuzzy logic calculations.

Function Breakdown:
1. `calculate_fuzzy_membership(value, fuzzy_set)`:
    - Calculates the fuzzy membership value of a given risk factor based on its fuzzy set.
    - Fuzzy logic is used to represent risk factors with some uncertainty (e.g., environmental risks).

2. `calculate_environmental_risk_with_fuzzy_logic(work_area, fuzzy_sets)`:
    - Calculates the environmental risk for a specific work area by summing up the fuzzy membership 
    values of all relevant risk factors in that area.

3. `calculate_all_work_areas_risk_fuzzy(input_file, fuzzy_file)`:
    - Loads the work area data and fuzzy sets from input files, and calculates the environmental 
    risk for each work area using fuzzy logic. 
    - Returns a dictionary mapping each work area to its calculated risk score.

4. `calculate_vulnerability_score(node)`:
    - Calculates the total vulnerability score for a node by summing up the CVSS (Common Vulnerability Scoring System) 
    scores of all known CVEs (Common Vulnerabilities and Exposures) associated with that node.

5. `calculate_centrality_scores(graph)`:
    - Calculates centrality scores for each node using **betweenness centrality**.
    - Centrality reflects how "central" a node is in the network, with higher centrality meaning more 
    importance and a bigger potential impact if attacked.

6. `calculate_connectedness_scores(graph)`:
    - Calculates the connectedness score for each node, based on the number of neighbors (degree) in the graph.
    - Nodes that are highly connected are penalized more heavily because their compromise could lead 
    to greater system-wide impact.

7. `calculate_switch_dependency(node)`:
    - Calculates the switch dependency for a node, which represents how reliant the node is on network switches.
    - Nodes with high switch dependency are more vulnerable to failures or attacks on the switches they rely on.

8. `calculate_redundancy(node)`:
    - Checks if the node has redundancy mechanisms (such as backups or SAN redundancy).
    - If redundancy exists, the node receives a bonus that mitigates some of the penalty from other factors.

9. `calculate_criticality(node, critical_function_weights)`:
    - Calculates the criticality score for a node based on the sum of its associated critical functions.
    - Critical nodes are more important to the organization's operations, and thus, their compromise would result 
    in a higher penalty to the resilience score.

10. `calculate_node_environmental_risk(node, fuzzy_scores, critical_function_to_work_area)`:
    - Calculates the environmental risk for a node by summing up the environmental risk scores of all the work areas 
    that its associated critical functions belong to.
    - The higher the environmental risk, the greater the reduction in resilience score.

11. `calculate_resilience_scores(nodes_data, graph, fuzzy_scores, critical_function_weights)`:
    - This is the core function that calculates the resilience score for each node.
    - It starts with a base score of 100, then applies penalties for CVEs, centrality, connectedness, 
    switch dependency, and criticality.
    - If redundancy exists, it provides a bonus to the score.
    - Finally, the score is divided by (1 + environmental risk factor), ensuring that nodes in riskier work 
    areas receive a lower final resilience score.

Process Summary:
- First, we load the node data and environmental risk factors.
- We then construct a graph based on the node connections to compute centrality and connectedness.
- Each node's resilience score is calculated by applying penalties for vulnerability, criticality, network dependency, and more.
- The environmental risk is applied at the end, reducing the score further based on work area conditions.
- The resilience scores are output for review and saved to a file for further analysis.
"""
