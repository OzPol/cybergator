from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from app.services.data_loader import get_nodes, save_nodes_data  # Save function added

def load_nodes_data():
    """Extract all nodes and their associated CVEs."""
    nodes_data = get_nodes()
    
    if not nodes_data:
        print("ERROR: No node data loaded!")  # Debugging
        return []

    formatted_data = [
        {
            "Node ID": node["node_id"],
            "Node Name": node["node_name"],
            "Node Type": node["node_type"],
            "Total CVEs": len(node.get("CVE", [])),  # Use get() to prevent errors
            "Max NVD Score": max(node.get("CVE_NVD", {}).values(), default=0),
            "Remove": "❌"  # Remove button
        }
        for node in nodes_data
    ]
    
    print(f"Nodes Loaded: {len(formatted_data)} entries")  # Debugging
    return formatted_data


def nodes_table_layout():
    """Render the Nodes Table Page with edit, add, and remove features."""
    nodes_data = load_nodes_data()

    return dbc.Container([
        html.H3("Nodes Table", className="text-center mt-4"),

        html.Div(
            dcc.Link(
                dbc.Button("Go to System Tables", color="primary", className="mb-3"),
                href="/system-tables"
            )
        ),

        # Search Bar for Live Filtering
        dcc.Input(id="node-search", type="text", placeholder="Search Nodes...", debounce=True),

        dash_table.DataTable(
            id="nodes-table",
            columns=[
                {"name": "Node ID", "id": "Node ID"},
                {"name": "Node Name", "id": "Node Name", "editable": True},
                {"name": "Node Type", "id": "Node Type", "editable": True},
                {"name": "Total CVEs", "id": "Total CVEs", "type": "numeric"},
                {"name": "Max NVD Score", "id": "Max NVD Score", "type": "numeric"},
                {"name": "Remove", "id": "Remove", "presentation": "markdown"},
            ],
            data=nodes_data, # Load data from JSON
            editable=True,  # Allows inline editing
            filter_action="native",
            sort_action="native",
            row_selectable="multi",
            page_size=15,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        ),
        
        # Add New Node Section
        html.H4("Add New Node"),
        dcc.Input(id="new-node-id", type="text", placeholder="Node ID"),
        dcc.Input(id="new-node-name", type="text", placeholder="Node Name"),
        dcc.Input(id="new-node-type", type="text", placeholder="Node Type"),
        dbc.Button("Add Node", id="add-node-btn", color="success"),
    ], fluid=True)

