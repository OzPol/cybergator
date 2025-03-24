from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from app.services.data_loader import get_software_inventory

def load_software_data():
    """Load software inventory nodes from the XLSX file."""
    software_data = get_software_inventory()
    
    if not software_data:
        print("ERROR: No software inventory data loaded!")
        return []

    formatted_data = [
        {
            "Category": entry.get("category", ""),
            "Rack Name": entry.get("rack_name", ""),
            "Node ID": entry.get("node_id", ""),
            "Node Name": entry.get("node_name", ""),
            "Is In Use": entry.get("is_in_use", ""),
            "Software ID": entry.get("software_id", ""),
            "Software Make": entry.get("software_make", ""),
            "Software Description": entry.get("software_description", ""),
            "Software Version": entry.get("software_version", ""),
            "Remove": "❌"
        }
        for entry in software_data
    ]

    print(f"Software Inventory Loaded: {len(formatted_data)} entries")
    return formatted_data

def software_table_layout():
    """Render the Software Inventory Table Page."""
    software_data = load_software_data()

    return dbc.Container([
        html.H3("Software Inventory Table", className="text-center mt-4"),

        html.Div(
            dcc.Link(
                dbc.Button("Go to System Tables", color="primary", className="mb-3"),
                href="/system-tables"
            )
        ),

        dcc.Input(id="software-search", type="text", placeholder="Search Software...", debounce=True),

        dash_table.DataTable(
            id="software-table",
            columns=[
                {"name": "Category", "id": "Category"},
                {"name": "Rack Name", "id": "Rack Name"},
                {"name": "Node ID", "id": "Node ID"},
                {"name": "Node Name", "id": "Node Name", "editable": True},
                {"name": "Is In Use", "id": "Is In Use"},
                {"name": "Software ID", "id": "Software ID"},
                {"name": "Software Make", "id": "Software Make"},
                {"name": "Software Description", "id": "Software Description"},
                {"name": "Software Version", "id": "Software Version"},
                {"name": "Remove", "id": "Remove", "presentation": "markdown"},
            ],
            data=software_data,
            editable=True,
            filter_action="native",
            sort_action="native",
            row_selectable="multi",
            page_size=15,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        ),

        html.Br(),

        # Display error messages
        html.Div(id="error-message", className="text-danger mt-2 text-center"),

        dbc.Row([
    # Category Dropdown (Rack or Workstation)
    dbc.Col([
        html.Label("Category:", className="fw-bold"),
        dcc.Dropdown(
            id="new-software-category",
            options=[
                {"label": "Rack", "value": "rack"},
                {"label": "Workstation", "value": "workstation"}
            ],
            placeholder="Select Category"
        )
    ], width=3),

    # Rack Type Dropdown
    dbc.Col([
        html.Label("Rack Type:", className="fw-bold"),
        dcc.Dropdown(
            id="new-rack-type",
            options=[
                {"label": "Boundary Defense Rack", "value": "boundary_defense_rack"},
                {"label": "Bulk Data Storage Rack", "value": "bulk_data_storage_rack"},
                {"label": "Server Rack", "value": "server_rack"},
                {"label": "Not a Rack", "value": "not_a_rack"}
            ],
            placeholder="Select Rack Type"
        )
    ], width=3),

    # Node ID 
    dbc.Col([
        html.Label("Node ID:", className="fw-bold"),
        dcc.Input(id="new-node-id", type="text", placeholder="Enter Node ID")
    ], width=2),

    # Is In Use 
    dbc.Col([
        html.Label("Is In Use:", className="fw-bold"),
        dcc.Dropdown(
            id="new-is-in-use",
            options=[
                {"label": "True", "value": "true"},
                {"label": "False", "value": "false"}
            ],
            placeholder="Select Status"
        )
    ], width=2),

    # Software ID 
    dbc.Col([
        html.Label("Software ID:", className="fw-bold"),
        dcc.Input(id="new-software-id", type="text", placeholder="Enter Software ID")
    ], width=2),
], className="mt-2"),

dbc.Row([
    # Software Make 
    dbc.Col([
        html.Label("Software Make:", className="fw-bold"),
        dcc.Input(id="new-software-make", type="text", placeholder="Enter Software Make")
    ], width=3),

    # Software Description
    dbc.Col([
        html.Label("Software Description:", className="fw-bold"),
        dcc.Input(id="new-software-description", type="text", placeholder="Enter Software Description")
    ], width=4),

    # Add Software Button
    dbc.Col([
        html.Label(" ", className="fw-bold"),  
        dbc.Button("Add Software", id="add-software-btn", color="success")
    ], width=2),
], className="mt-2"),
    ], fluid=True)
    