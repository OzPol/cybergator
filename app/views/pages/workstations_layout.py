from dash import html, dcc, Input, Output, State, callback, ctx, ALL
import dash_bootstrap_components as dbc
import json
import os

# Load JSON
risk_data_path = os.path.join("app", "data", "json", "Risk_Factors.json")
with open(risk_data_path, "r") as f:
    risk_data = json.load(f)

work_areas = risk_data["work_areas"]
risk_factors_matrix = risk_data["Risk_Factors_Matrix"]

change_log = []
change_count = 0

# Layout
def workstation_cards():
    cards = []

    for idx, area in enumerate(work_areas):
        work_area = area["Work_Area"]
        factors = area["Risk_Factors"]

        factor_controls = []
        for factor, value in factors.items():
            options = risk_factors_matrix.get(factor, ["Yes", "No", "NA"])
            factor_controls.append(
                dbc.Row([
                    dbc.Col(html.Div(factor.replace("_", " ").capitalize(), className="fw-bold"), width=6),
                    dbc.Col(
                        dbc.ButtonGroup([
                            dbc.Button(
                                opt,
                                id={"type": "btn-option", "area": work_area, "factor": factor, "value": opt},
                                color="primary" if opt == value else "secondary",
                                outline=opt != value,
                                size="sm",
                                className="me-1"
                            ) for opt in options
                        ], size="sm"),
                        width=6
                    )
                ], className="mb-2")
            )

        card = dbc.Card([
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col(html.H5(work_area.replace("_", " "), className="mb-0"), width=10),
                    dbc.Col(
                        dbc.Button("View Risk Factors", id={"type": "toggle-button", "index": idx},
                                   color="primary", size="sm", className="float-end"),
                        width=2, style={"textAlign": "right"}
                    )
                ], align="center")
            ),
            dbc.Collapse(
                dbc.CardBody(factor_controls, className="bg-light rounded shadow-sm p-3"),
                id={"type": "collapse", "index": idx},
                is_open=False
            )
        ], className="mb-4 shadow-sm rounded")

        cards.append(card)

    return dbc.Container([
        html.H2("Work Stations", className="text-center mt-4"),
        html.P("Explore and modify risk factors by work area.", className="text-center mb-4"),
        dbc.Row(dbc.Col(cards, width=12)),  # ✅ Single column stacking all cards
        html.Div(id="update-status", className="text-success text-center mt-2"),
        html.Div(id="change-counter", className="text-center text-info mt-2 fw-bold"),
        html.Details([
            html.Summary("Change Log", className="text-primary mb-2 text-center"),
            html.Ul(id="change-log", className="text-center list-unstyled")
        ], open=False, className="mt-3")
    ], fluid=True)

# Collapse toggle
@callback(
    Output({"type": "collapse", "index": ALL}, "is_open"),
    Input({"type": "toggle-button", "index": ALL}, "n_clicks"),
    State({"type": "collapse", "index": ALL}, "is_open"),
)
def toggle_collapse(n_clicks_list, is_open_list):
    ctx_id = ctx.triggered_id
    if ctx_id is None:
        return is_open_list

    clicked_idx = ctx_id["index"]
    return [not open_ if i == clicked_idx else open_ for i, open_ in enumerate(is_open_list)]

# Button selection callback
@callback(
    Output("update-status", "children"),
    Output("change-log", "children"),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "color"),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "outline"),
    Input({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "n_clicks"),
    State({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "id"),
    prevent_initial_call=True
)
def update_button_selection(n_clicks, ids):
    global change_log, change_count
    new_logs = []
    changes_made = 0
    updated_colors = []
    updated_outlines = []

    with open(risk_data_path, "r") as f:
        data = json.load(f)

    latest_selections = {}

    for idx, (n, id_obj) in enumerate(zip(n_clicks, ids)):
        area = id_obj["area"]
        factor = id_obj["factor"]
        val = id_obj["value"]

        for entry in data["work_areas"]:
            if entry["Work_Area"] == area:
                current = entry["Risk_Factors"].get(factor)
                if ctx.triggered_id == id_obj:
                    if current != val:
                        entry["Risk_Factors"][factor] = val
                        changes_made += 1
                        new_logs.append(html.Li(
                            f"{area.replace('_', ' ')}: '{factor.replace('_', ' ')}' changed from '{current}' to '{val}'"
                        ))
                latest_selections[f"{area}|{factor}"] = entry["Risk_Factors"][factor]

    if changes_made:
        with open(risk_data_path, "w") as f:
            json.dump(data, f, indent=4)
        change_count += changes_made
        change_log = new_logs + change_log

    for id_obj in ids:
        area = id_obj["area"]
        factor = id_obj["factor"]
        val = id_obj["value"]
        current_val = latest_selections.get(f"{area}|{factor}")
        if val == current_val:
            updated_colors.append("primary")
            updated_outlines.append(False)
        else:
            updated_colors.append("secondary")
            updated_outlines.append(True)

    status_msg = f"{change_count} Change{'s' if change_count != 1 else ''} saved ✅" if changes_made else "No changes made"
    return status_msg, change_log, updated_colors, updated_outlines
