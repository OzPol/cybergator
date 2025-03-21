from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from app.services.data_loader import get_nodes  # Load data from Nodes_Complete.json
from app.services.data_loader import get_all_nodes, get_all_software

def load_cve_data():
    """Extract CVEs, their NVD scores, and affected nodes, fully flattened."""
    nodes_data = get_nodes()  # Load nodes from JSON
    cve_list = []

    for idx, node in enumerate(nodes_data):
        for cve_id, nvd_score in node["CVE_NVD"].items():
            cve_list.append({
                "CVE ID": cve_id,
                "NVD Score": nvd_score,
                "Node ID": node["node_id"],
                "Node Name": node["node_name"],
                "Remove": "❌"
            })
    return cve_list

def cves_table_layout():
    # Render the CVEs Table Page with Add Functionality.
    cve_data = load_cve_data()  # Fetch CVEs from Nodes_Complete.json
    software_options = get_all_software()  # Get software list for dropdown
    # Prepare dropdowns for makes and versions
    software_make_options = [{"label": make, "value": make} for make in software_options.keys()]
    
    
    return dbc.Container([
        html.H3("CVEs Table", className="text-center mt-4"),

        html.Div(
            dcc.Link(
                dbc.Button("Go to System Tables", color="primary", className="mb-3"),
                href="/system-tables"
            )
        ),

        # CVE Search Bar
        dcc.Input(id="cve-search", type="text", placeholder="Search CVEs...", debounce=True),

        dash_table.DataTable(
            id="cves-table",
            columns=[
                {"name": "CVE ID", "id": "CVE ID", "editable": True},
                {"name": "NVD Score", "id": "NVD Score", "type": "numeric", "editable": True},
                {"name": "Node ID", "id": "Node ID", "editable": True},
                {"name": "Node Name", "id": "Node Name", "editable": True},
                {"name": "Remove", "id": "Remove", "presentation": "markdown"}, 
            ],
            data=cve_data,
            editable=True,
            row_selectable="multi",  # Allow selection of rows
            filter_action="native",
            sort_action="native",
            page_size=50,  # Display 50 CVEs per page
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
            
            derived_viewport_data=cve_data,
        ),

        html.Br(),
        
        # Display error messages
        html.Div(id="error-message", className="text-danger mt-2 text-center"),

        # Add New CVE Section
        html.H4("Add New CVE", className="text-center mt-4"),
        dbc.Row([
            dbc.Col(dcc.Input(id="new-cve-id", type="text", placeholder="CVE ID"), width=3),
            # Select NVD Score (Readonly, fetched automatically)
            dbc.Col(dcc.Input(id="new-nvd-score", type="number", placeholder="NVD Score", disabled=True), width=3),

            # Select Software Make
            dbc.Col(dcc.Dropdown(
                id="new-software-make",
                options=software_make_options,
                placeholder="Select Software Make",
            ), width=3),

            # Select Software Version (Filtered on Make)
            dbc.Col(dcc.Dropdown(
                id="new-software-version",
                options=[],  # Will be populated dynamically
                placeholder="Select Software Version",
            ), width=3),
            
            dbc.Col(dbc.Button("Add CVE", id="add-cve-btn", color="success"), width=2),
        ], className="mt-2"),
    ], fluid=True)