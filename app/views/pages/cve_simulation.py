from dash import html, dcc, dash_table, Input, Output, State, callback
import dash_bootstrap_components as dbc
import uuid

# Initial empty data store
def get_initial_cve_data():
    return []

def cve_simulation_layout():
    return dbc.Container([
        html.H3("CVE Simulation Table", className="text-center mt-4"),

        dcc.Store(id="cve-sim-store", data=get_initial_cve_data()),

        dash_table.DataTable(
            id="cve-simulation-table",
            columns=[
                {"name": "CVE ID", "id": "CVE ID", "editable": True},
                {"name": "NVD Score", "id": "NVD Score", "type": "numeric", "editable": True},
                {"name": "Node ID", "id": "Node ID", "editable": True},
                {"name": "Node Name", "id": "Node Name", "editable": True},
                {"name": "Remove", "id": "Remove", "presentation": "markdown"},
            ],
            data=[],
            editable=True,
            row_deletable=False,
            filter_action="native",
            sort_action="native",
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"}
        ),

        html.Hr(),
        html.H4("Add New CVE", className="mt-3"),

        dbc.Row([
            dbc.Col(dcc.Input(id="input-cve-id", type="text", placeholder="CVE ID"), width=2),
            dbc.Col(dcc.Input(id="input-nvd-score", type="number", placeholder="NVD Score"), width=2),
            dbc.Col(dcc.Input(id="input-node-id", type="text", placeholder="Node ID"), width=2),
            dbc.Col(dcc.Input(id="input-node-name", type="text", placeholder="Node Name"), width=3),
            dbc.Col(dcc.Input(id="input-resilience", type="number", placeholder="Resilience Score"), width=2),
            dbc.Col(dbc.Button("Add CVE", id="add-cve-btn", color="success"), width=1),
        ], className="mb-4"),

        html.Div(id="reset-confirmation", className="text-success mt-2")
    ], fluid=True)

@callback(
    Output("cve-simulation-table", "data"),
    Output("cve-sim-store", "data"),
    Input("add-cve-btn", "n_clicks"),
    State("input-cve-id", "value"),
    State("input-nvd-score", "value"),
    State("input-node-id", "value"),
    State("input-node-name", "value"),
    State("input-resilience", "value"),
    State("cve-sim-store", "data"),
    prevent_initial_call=True
)
def add_cve(n_clicks, cve_id, nvd_score, node_id, node_name, resilience, current_data):
    new_row = {
        "CVE ID": cve_id or f"CVE-{uuid.uuid4().hex[:6]}",
        "NVD Score": nvd_score or 0.0,
        "Node ID": node_id or "N/A",
        "Node Name": node_name or "Unnamed Node",
        "Resilience Score": resilience or "N/A",
        "Remove": "❌"
    }
    current_data.append(new_row)
    return current_data, current_data