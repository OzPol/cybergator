# app/views/pages/graph_controls.py
from dash import dcc, html
import dash_bootstrap_components as dbc

layout_options = [
    "grid", "circle", "concentric", "breadthfirst", "cose", "cola", "random"
]

def render_graph_controls():
    return html.Div([
        html.H5("Graph Controls", className="text-center mb-3"),

        dcc.Tabs(id="graph-controls-tabs", value="layout-tab", children=[
            dcc.Tab(label="Layout", value="layout-tab", children=[
                html.Div([
                    html.Label("Layout:"),
                    dcc.Dropdown(
                        id="layout-dropdown",
                        options=[{"label": name.capitalize(), "value": name} for name in layout_options],
                        value="grid",
                        clearable=False,
                        style={"marginBottom": "10px"}
                    )
                ])
            ]),
            dcc.Tab(label="Stylesheet JSON", value="style-tab", children=[
                html.Div([
                    html.P("Custom styles will go here.")
                ])
            ]),
            dcc.Tab(label="Elements JSON", value="elements-tab", children=[
                html.Div([
                    html.P("Element info and debug tools will go here.")
                ])
            ])
        ])
    ], style={"padding": "10px"})
