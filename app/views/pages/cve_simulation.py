from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from app.services.data_loader import get_nodes, get_all_software, reset_nodes_data

def load_cve_data():
    """Extract CVEs, their NVD scores, and affected nodes, fully flattened."""
    reset_nodes_data()
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

def cve_simulation_layout(session_user=None, resilience_score=None):
    # Render the CVEs Table Page with Add Functionality.
    cve_data = load_cve_data()  # Fetch CVEs from Nodes_Complete.json
    software_options = get_all_software()  # Get software list for dropdown
    # Prepare dropdowns for makes and versions
    software_make_options = [{"label": make, "value": make} for make in software_options.keys()]

    return dbc.Container([
        html.H3("Common Vulnerabilities and Exposures Simulation", className="text-center mt-4"),
        
        html.Div([
            html.P("The Common Vulnerabilities and Exposures (CVE) Simulation allows users to evaluate their system’s security "
            "weaknesses by analyzing known vulnerabilities within the System Under Evaluation (SUE). This tool helps identify "
            "critical flaws and prioritize security patches based on risk levels."),
            
            html.H5("How it Works"),
            html.Ul([
                html.Li("Automated CVE Lookup – The simulation pulls real-time vulnerability data from known security databases,"
                " such as the National Vulnerability Database (NVD)."),
                html.Li("Severity-Based Risk Assessment – Each CVE is assigned a score based on industry-standard severity metrics"
                " (e.g., CVSS scores), helping users determine the most pressing security risks."),
                html.Li("System-Wide Impact Evaluation – The simulation scans all components of the SUE and generates a list of"
                " affected assets, highlighting the extent of exposure.")
            ]),

            html.H5("Key Features"),
            html.Ul([
                html.Li("Table of Present CVEs – Displays a comprehensive list of known vulnerabilities within the system."),
                html.Li("Number of Affected Items – Shows how many system components (workstations, servers, or other assets) "
                "are currently impacted by each CVE."),
                html.Li("Prioritization Tools – Users can sort and filter vulnerabilities based on severity, number of affected"
                " nodes, or criticality to system operations.")
            ]),

            html.P("Users can interact with this table to:"),
            html.Ul([
                html.Li("✔ Expand details about each CVE, including affected software versions and known exploits."),
                html.Li("✔ Mark vulnerabilities as patched after applying security updates."),
                html.Li("✔ Export vulnerability reports for documentation and compliance tracking.")
            ]),

            html.H5("Why Use the CVE Simulation?"),
            html.Ul([
                html.Li("Proactive Security – Helps cybersecurity teams identify high-risk vulnerabilities before they are exploited."),
                html.Li("Resource Optimization – Prioritizes which security patches should be implemented first based on impact."),
                html.Li("Risk Reduction – Provides insights into which system components are most vulnerable, allowing users to"
                " reinforce critical assets.")
            ]),

            html.P("By running CVE Simulations, users gain a comprehensive view of their system’s security posture, ensuring that"
            " the most critical vulnerabilities are addressed before they can be exploited."),
        ], className="mb-4"),
        
        html.Div(
            f"Simulated Resilience Score: {resilience_score if resilience_score is not None else 'N/A'}",
            style={'textAlign': 'right', 'marginTop': '20px', 'fontSize': '1.2rem'}
        ),

        html.Div(
            dcc.Link(
                dbc.Button("CVE Refresh", color="primary", className="mb-3"),
                href="/cve-simulation",
                refresh=True
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