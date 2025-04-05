import dash
from dash import html, dcc, Input, Output, State, callback, ctx, ALL
import dash_bootstrap_components as dbc
import json
import os

# Load JSON
risk_data_path = os.path.join("app", "data", "json", "Risk_Factors.json")
backup_data_path = os.path.join("app", "data", "backup", "Risk_Factors.json")

with open(risk_data_path, "r") as f:
    risk_data = json.load(f)

work_areas = risk_data["work_areas"]
risk_factors_matrix = risk_data["Risk_Factors_Matrix"]

change_log = []
change_count = 0

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
                        html.Div([
                            dbc.Button(
                                opt,
                                id={"type": "btn-option", "area": work_area, "factor": factor, "value": opt},
                                color="primary" if opt == value else "secondary",
                                outline=opt != value,
                                size="sm",
                                className="me-1 mb-1 d-inline-block"
                            ) for opt in options
                        ], style={"display": "flex", "flexWrap": "wrap"}),
                        width=6
                    )
                ], className="mb-2")
            )

        factor_controls.append(
            dbc.Button("Reset Work Area", id={"type": "reset-button", "area": work_area}, color="danger", size="sm", className="mt-2")
        )

        card = dbc.Card([
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col(
                        html.H5(work_area.replace("_", " "), className="mb-0"),
                        xs=12, md=8, className="d-flex align-items-center"
                    ),
                    dbc.Col(
                        dbc.Button("View Risk Factors", id={"type": "toggle-button", "index": idx},
                                color="primary", size="sm", className="w-100"),
                        xs=12, md=4, className="mt-2 mt-md-0"
                    )
                ], className="g-1")
            ),
            dbc.Collapse(
                dbc.CardBody(factor_controls, className="bg-light rounded shadow-sm p-3"),
                id={"type": "collapse", "index": idx},
                is_open=False
            )
        ], className="shadow-sm rounded")  # Removed h-100 class

        # Wrap each card in its own column that will maintain its own layout
        card_col = dbc.Col(
            card,
            width=12, md=6, lg=4, 
            className="mb-4",
            style={"display": "flex", "flex-direction": "column"}
        )
        
        cards.append(card_col)
    
    # Create rows with 3 cards each
    card_rows = []
    for i in range(0, len(cards), 3):
        card_row = dbc.Row(
            cards[i:i+3],
            className="g-3",  # Add gutter spacing between cards
        )
        card_rows.append(card_row)
    
    return dbc.Container([
        html.H2("Work Stations", className="text-center mt-4"),
        html.P("Explore and modify risk factors by work area.", className="text-center mb-4"),
        html.Div(card_rows),  # Use the new card rows layout
        html.Div(id="update-status", className="text-success text-center mt-2"),
        html.Div(id="change-counter", className="text-center text-info mt-2 fw-bold"),
        html.Details([
            html.Summary("Change Log", className="text-primary mb-2 text-center"),
            html.Ul(id="change-log", className="text-center list-unstyled")
        ], open=False, className="mt-3")
    ], fluid=True)


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

@callback(
    Output("update-status", "children", allow_duplicate=True),
    Output("change-log", "children", allow_duplicate=True),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "color", allow_duplicate=True),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "outline", allow_duplicate=True),
    Input({"type": "reset-button", "area": ALL}, "n_clicks"),
    State({"type": "reset-button", "area": ALL}, "id"),
    State({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "id"),
    prevent_initial_call=True
)
def reset_work_area(n_clicks, reset_ids, button_ids):
    global change_log, change_count
    if not any(n_clicks):
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    triggered_area = ctx.triggered_id["area"]

    with open(backup_data_path, "r") as f:
        backup_data = json.load(f)
    with open(risk_data_path, "r") as f:
        current_data = json.load(f)

    backup_entry = next((wa for wa in backup_data["work_areas"] if wa["Work_Area"] == triggered_area), None)
    current_entry = next((wa for wa in current_data["work_areas"] if wa["Work_Area"] == triggered_area), None)

    if not backup_entry or not current_entry:
        return f"Error: Work area not found", change_log, dash.no_update, dash.no_update

    # Reset all values for this work area to defaults
    changes_made = 0
    for factor, default_value in backup_entry["Risk_Factors"].items():
        if current_entry["Risk_Factors"].get(factor) != default_value:
            changes_made += 1
            current_entry["Risk_Factors"][factor] = default_value

    # Save changes to the current data file
    with open(risk_data_path, "w") as f:
        json.dump(current_data, f, indent=4)

    # Remove all change log entries for this specific work area
    filtered_log = [log for log in change_log if not log.children.startswith(triggered_area.replace('_', ' '))]
    
    # Update change count
    change_count = len(filtered_log)
    
    # Update the change log
    change_log = filtered_log

    # Update button colors and outlines
    latest = {wa["Work_Area"]: wa["Risk_Factors"] for wa in current_data["work_areas"]}
    colors, outlines = [], []
    for btn in button_ids:
        a, f_, v = btn["area"], btn["factor"], btn["value"]
        current_val = latest[a][f_]
        colors.append("primary" if current_val == v else "secondary")
        outlines.append(current_val != v)

    status_msg = f"{triggered_area.replace('_', ' ')} reset to default values ✅"
    
    return status_msg, change_log, colors, outlines

@callback(
    Output("update-status", "children", allow_duplicate=True),
    Output("change-log", "children", allow_duplicate=True),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "color", allow_duplicate=True),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "outline", allow_duplicate=True),
    Output("change-counter", "children", allow_duplicate=True),
    Input("reset-work-areas", "n_clicks"),
    State({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "id"),
    prevent_initial_call=True
)
def reset_all_work_areas(n_clicks, button_ids):
    global change_log, change_count
    if not n_clicks:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Load backup data
    with open(backup_data_path, "r") as f:
        backup_data = json.load(f)
    # Load current data
    with open(risk_data_path, "r") as f:
        current_data = json.load(f)

    # For each work area in backup data
    for backup_area in backup_data["work_areas"]:
        area_name = backup_area["Work_Area"]
        # Find corresponding current area
        current_area = next((wa for wa in current_data["work_areas"] if wa["Work_Area"] == area_name), None)
        
        if current_area:
            # For each risk factor in this area
            for factor, default_value in backup_area["Risk_Factors"].items():
                current_area["Risk_Factors"][factor] = default_value

    # Save changes to the current data file
    with open(risk_data_path, "w") as f:
        json.dump(current_data, f, indent=4)

    # Reset the change count and log
    change_count = 0
    change_log = []

    # Update button colors and outlines
    latest = {wa["Work_Area"]: wa["Risk_Factors"] for wa in current_data["work_areas"]}
    colors, outlines = [], []
    for btn in button_ids:
        a, f_, v = btn["area"], btn["factor"], btn["value"]
        current_val = latest[a][f_]
        colors.append("primary" if current_val == v else "secondary")
        outlines.append(current_val != v)

    status_msg = "All work areas reset to default values ✅"
    # Clear the change counter text
    counter_msg = ""
    
    return status_msg, [], colors, outlines, counter_msg