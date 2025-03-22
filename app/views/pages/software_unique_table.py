from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from app.services.data_loader import get_software_cves, get_next_software_id, save_json

def load_unique_software():
    """Load unique software from software_cves.json."""
    software_data = get_software_cves()

    software_list = []
    for sw_id, details in software_data.items():
        software_list.append({
            "Software ID": sw_id,
            "Make": details.get("make", ""),
            "Description": details.get("description", ""),
            "Version": details.get("version", ""),
            "Expand": "➕",
            "Remove": "❌"
        })

    return software_list

def software_unique_table_layout():
    """Render the Unique Software Table Page."""
    unique_software_data = load_unique_software()

    return dbc.Container([
        html.H3("Unique Software Table", className="text-center mt-4"),

        html.Div(
            dcc.Link(
                dbc.Button("Go to System Tables", color="primary", className="mb-3"),
                href="/system-tables"
            )
        ),

        dcc.Input(id="software-unique-search", type="text", placeholder="Search Software...", debounce=True),

        dash_table.DataTable(
            id="software-unique-table",
            columns=[
                {"name": "Software ID", "id": "Software ID"},
                {"name": "Make", "id": "Make"},
                {"name": "Description", "id": "Description"},
                {"name": "Version", "id": "Version"},
                {"name": "Expand", "id": "Expand", "presentation": "markdown"},
                {"name": "Remove", "id": "Remove", "presentation": "markdown"},
            ],
            data=unique_software_data,
            editable=False,
            filter_action="native",
            sort_action="native",
            row_selectable="multi",
            page_size=20,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
        ),

        html.Div(id="expanded-software-details", className="mt-4"),

        html.H4("Add New Software", className="text-center mt-4"),
        dbc.Row([
            dbc.Col(dcc.Input(id="new-software-make", type="text", placeholder="Software Make"), width=3),
            dbc.Col(dcc.Input(id="new-software-desc", type="text", placeholder="Software Description"), width=3),
            dbc.Col(dcc.Input(id="new-software-version", type="text", placeholder="Software Version"), width=3),
            dbc.Col(dbc.Button("Add Software", id="add-software-btn", color="success"), width=2),
        ], className="mt-2"),

        html.Div(id="error-message", className="text-danger mt-2 text-center"),
    ], fluid=True)
