import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import os

matplotlib.use('Agg')  

def generate_graph_system(json_data):
    """Generate a system graph from JSON data and save it as an image."""
    
    if not json_data:
        print("⚠ No data available to generate the graph.")
        return
    
    G = nx.Graph()

    # Node labels
    labels = {}
    
    # Lists to store node shapes
    square_nodes = []
    circle_nodes = []

    # Add nodes to the graph with properties from JSON
    for node in json_data:
        node_id = node['node_id']
        node_name = node['node_name']
        node_type = node['node_type']
        
        # Assign labels based on node type
        labels[node_id] = node_name if node_type in ['Firewall', 'Router'] else node_id

        # Assign nodes to either squares or circles
        if node_type in ['Switch', 'Firewall', 'Router']:  # Square nodes
            square_nodes.append(node_id)
        else:  # Circle nodes for all other types
            circle_nodes.append(node_id)

        G.add_node(node_id, label=node_name)

    # Add edges (connections between nodes)
    for node in json_data:
        node_id = node['node_id']
        connected_nodes = node.get('connected_to', [])
        for connected_node in connected_nodes:
            G.add_edge(node_id, connected_node)
    
    # Use spring layout
    pos = nx.spring_layout(G, seed=10, k=0.2)

    # Plot the graph
    plt.figure(figsize=(18, 10))
    
    # Draw the square nodes (Switches, Firewalls, Routers)
    nx.draw_networkx_nodes(G, pos, nodelist=square_nodes, node_shape='s', node_color='lightblue', node_size=2000)
    
    # Draw the circle nodes (everything else)
    nx.draw_networkx_nodes(G, pos, nodelist=circle_nodes, node_shape='o', node_color='lightgreen', node_size=1500)
    
    # Draw the edges and labels
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title('System Information Architecture Graph')

    # Save to /app/assets inside docker
    # Locally, it will be created inside cybergator/assets
    assets_dir = "/app/assets"
    os.makedirs(assets_dir, exist_ok=True)
    output_path = os.path.join(assets_dir, "system_graph.png")

    plt.savefig(output_path)
    plt.close()

    return output_path
