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
        )
    ], fluid=True)
    