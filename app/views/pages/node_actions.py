from dash import html, dcc
from app.services.data_loader import (
    get_node_types,
    get_software_dropdown_options,
    get_rack_options,
    get_critical_function_keys,
    get_all_nodes
)
import dash_bootstrap_components as dbc

def render_node_controls():
    make_options, _ = get_software_dropdown_options()

    return html.Div([
        html.H5("Node Controls", style={"marginBottom": "10px"}),

        dcc.Input(
            id="node-id-input",
            type="text",
            placeholder="Node ID",
            debounce=True,
            style={"marginBottom": "10px", "width": "100%"}
        ),

        dcc.Input(
            id="node-name-input",
            type="text",
            placeholder="Node Name",
            debounce=True,
            style={"marginBottom": "10px", "width": "100%"}
        ),

        dcc.Dropdown(
            id="node-type-selector",
            options=[{"label": t, "value": t} for t in get_node_types()],
            placeholder="Select Node Type",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="rack-selector",
            options=get_rack_options(),
            placeholder="Select Rack",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="category-selector",
            options=[
                {"label": "rack", "value": "rack"},
                {"label": "workstation", "value": "workstation"},
                {"label": "other", "value": "other"}
            ],
            placeholder="Select Category",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="critical-function-selector",
            options=[{"label": f, "value": f} for f in get_critical_function_keys()],
            multi=True,
            placeholder="Select Critical Functions",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="connected-nodes-selector",
            options=get_all_nodes(),
            multi=True,
            placeholder="Connect To Nodes",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="backup-role",
            options=[
                {"label": "Primary", "value": "Primary"},
                {"label": "Secondary", "value": "Secondary"},
                {"label": "None", "value": "null"}
            ],
            placeholder="Select Backup Role",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="data-redundancy-selector",
            options=[
                {"label": "Yes", "value": "Yes"},
                {"label": "No", "value": "No"}
            ],
            placeholder="Data Redundancy",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="risk-factor-selector",
            options=[
                {"label": "High", "value": "High"},
                {"label": "Medium", "value": "Medium"},
                {"label": "Low", "value": "Low"}
            ],
            placeholder="Risk Factor",
            style={"marginBottom": "10px"}
        ),

        dcc.Checklist(
            id="switch-dependency-check",
            options=[{"label": "Switch Dependency", "value": "yes"}],
            style={"marginBottom": "10px"}
        ),

        dcc.Input(
            id="resilience-penalty-input",
            type="number",
            value=0.1,
            disabled=True,
            placeholder="Auto-calculated later",
            style={"marginBottom": "10px", "width": "100%", "backgroundColor": "#f1f1f1", "color": "#888"}
        ),

        dcc.Dropdown(
            id="software-make-selector",
            options=make_options,
            placeholder="Select Software Make",
            style={"marginBottom": "10px"}
        ),

        dcc.Dropdown(
            id="software-version-selector",
            placeholder="Select Software Version",
            style={"marginBottom": "10px"}
        ),

        html.Button(
            "Create Node",
            id="submit-new-node",
            n_clicks=0,
            style={"width": "100%", "marginBottom": "10px"}
        ),

        html.Div(id="node-feedback", style={"color": "green", "fontSize": "12px"})
    ], style={
        "border": "1px solid #ccc",
        "padding": "15px",
        "borderRadius": "5px",
        "backgroundColor": "#f9f9f9"
    })
