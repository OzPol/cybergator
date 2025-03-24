from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from app.services.data_loader import get_hardware_inventory

def load_hardware_data():
    hardware_data = get_hardware_inventory()

    if not hardware_data:
        print("ERROR: No hardware inventory data loaded!")
        return []
    
    formatted_data = [
        {
            "Category": entry.get("category", ""),
            "Rack Name": entry.get("rack_name", ""),
            "Hardware ID": entry.get("hardware_id", ""),
            "Hardware Make": entry.get("hardware_make", ""),
            "Hardware Model": entry.get("hardware_model", ""),
            "Node ID": entry.get("node_id", ""),
            "Hardware Description": entry.get("hardware_description", ""),
            "Remove": "❌"
        }
        for entry in hardware_data
    ]

    print(f"Hardware Inventory Loaded: {len(formatted_data)} entries")
    return formatted_data


def hardware_table_layout():
    """Render the Hardware Inventory Table Page."""
    hardware_data = load_hardware_data()

    return dbc.Container([
        html.H3("Hardware Inventory Table", className="text-center mt-4"),

        html.Div(
            dcc.Link(
                dbc.Button("Go to System Tables", color="primary", className="mb-3"),
                href="/system-tables"
            )
        ),

        dcc.Input(id="hardware-search", type="text", placeholder="Search Hardware...", debounce=True),

        dash_table.DataTable(
            id="hardware-table",
            columns=[
                {"name": "Category", "id": "Category"},
                {"name": "Rack Name", "id": "Rack Name"},
                {"name": "Hardware ID", "id": "Hardware ID"},
                {"name": "Hardware Make", "id": "Hardware Make", "editable": True},
                {"name": "Hardware Model", "id": "Hardware Model"},
                {"name": "Node ID", "id": "Node ID"},
                {"name": "Hardware Description", "id": "Hardware Description"},
                {"name": "Remove", "id": "Remove", "presentation": "markdown"},
            ],
            data=hardware_data,
            editable=True,
            filter_action="native",
            sort_action="native",
            row_selectable="multi",
            page_size=15,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        )
    ], fluid=True)
    