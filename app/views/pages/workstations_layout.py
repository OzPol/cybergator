from dash import html, Input, Output, State, callback, ctx, ALL, no_update
import dash_bootstrap_components as dbc
import json
import os

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# Load JSON
risk_data_path = os.path.join("app", "data", "json", "Risk_Factors.json")
backup_data_path = os.path.join("app", "data", "backup", "Risk_Factors.json")

change_log = []
change_count = 0

def get_workstation_cards():

    risk_data = load_json(risk_data_path)
    work_areas = risk_data["work_areas"]
    risk_factors_matrix = risk_data["Risk_Factors_Matrix"]


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
    html.Div([
            dbc.Button("Reset Work Area", id={"type": "reset-button", "area": work_area}, color="danger", size="sm", className="me-2"),
            dbc.Button("❌ Delete", id={"type": "delete-button", "area": work_area}, color="secondary", size="sm"),
        ], className="d-flex gap-2 mt-2")
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
        ], className="shadow-sm rounded")

        # Wrap each card in its own column that will maintain its own layout
        card_col = dbc.Col(
            card,
            width=12, md=6, lg=4, 
            className="mb-4",
            style={"display": "flex", "flex-direction": "column"}
        )
        
        cards.append(card_col)

    # Add button as a new card
    add_card = dbc.Col(
        dbc.Button("➕ Add Work Area", id="open-add-modal", color="success", className="w-100"),
        width=12, md=6, lg=4,
        className="mb-4 d-flex align-items-start justify-content-center"
    )
    cards.append(add_card)
    
    # Create rows with 3 cards each
    card_rows = []
    for i in range(0, len(cards), 3):
        card_row = dbc.Row(
            cards[i:i+3],
            className="g-3",  # Add gutter spacing between cards
        )
        card_rows.append(card_row)
    
    return card_rows

def workstation_cards():
    """Main layout component for workstation cards"""
    card_rows = get_workstation_cards()
    
    return dbc.Container([
        html.H2("Work Stations", className="text-center mt-4"),
        html.P("Explore and modify risk factors by work area.", className="text-center mb-4"),
        html.Div(id="workstations-container", children=card_rows),  # Container for dynamically updated cards
        html.Div(id="update-status", className="text-success text-center mt-2"),
        html.Div(id="change-counter", className="text-center text-info mt-2 fw-bold"),
        html.Details([
            html.Summary("Change Log", className="text-primary mb-2 text-center"),
            html.Ul(id="change-log", className="text-center list-unstyled")
        ], open=False, className="mt-3"),
        # Add Work Area Modal
        dbc.Modal([
            dbc.ModalHeader("Create New Work Area"),
            dbc.ModalBody([
                dbc.Input(id="new-workarea-name", placeholder="Enter new work area name...", type="text"),
            ]),
            dbc.ModalFooter([
                dbc.Button("Add", id="confirm-add-workarea", color="primary", className="me-2"),
                dbc.Button("Cancel", id="cancel-add-modal", color="secondary")
            ])
        ], id="add-workarea-modal", is_open=False, backdrop="static"),
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
    
    if not ctx.triggered_id:
        return no_update, no_update, no_update, no_update
    
    # Get the clicked button info
    clicked_area = ctx.triggered_id["area"]
    clicked_factor = ctx.triggered_id["factor"]
    clicked_value = ctx.triggered_id["value"]
    
    with open(risk_data_path, "r") as f:
        data = json.load(f)
    
    new_logs = []
    changes_made = 0
    
    # Find the work area and make changes
    for entry in data["work_areas"]:
        if entry["Work_Area"] == clicked_area:
            current = entry["Risk_Factors"].get(clicked_factor)
            if current != clicked_value:
                entry["Risk_Factors"][clicked_factor] = clicked_value
                changes_made += 1
                new_logs.append(html.Li(
                    f"{clicked_area.replace('_', ' ')}: '{clicked_factor.replace('_', ' ')}' changed from '{current}' to '{clicked_value}'"
                ))
    
    # Save changes if any were made
    if changes_made:
        with open(risk_data_path, "w") as f:
            json.dump(data, f, indent=4)
        change_count += changes_made
        change_log = new_logs + change_log
    
    # Update button colors and outlines for ALL buttons
    # This is where we need to avoid selective updates that broke the page
    updated_colors = []
    updated_outlines = []
    
    for id_obj in ids:
        area = id_obj["area"]
        factor = id_obj["factor"]
        val = id_obj["value"]
        
        # Find the current selected value for this button's factor
        current_val = None
        for entry in data["work_areas"]:
            if entry["Work_Area"] == area:
                current_val = entry["Risk_Factors"].get(factor)
                break
        
        # Set appropriate color and outline
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
    
    # Fixed: Check if any buttons were clicked, and handle the empty ALL selector case
    if not n_clicks or not any(n_clicks):
        # Return no_update to prevent the callback from executing
        return no_update, no_update, no_update, no_update

    triggered_area = ctx.triggered_id["area"]

    with open(risk_data_path, "r") as f:
        current_data = json.load(f)
    with open(backup_data_path, "r") as f:
        backup_data = json.load(f)

    backup_names = {wa["Work_Area"] for wa in backup_data["work_areas"]}
    is_user_created = triggered_area not in backup_names

    current_entry = next((wa for wa in current_data["work_areas"] if wa["Work_Area"] == triggered_area), None)
    if not current_entry:
        # Fixed: Return no_update instead of empty lists
        return f"Error: Work area not found", change_log, no_update, no_update

    changes_made = 0

    if is_user_created:
        # Set all risk factors to ""
        for factor in current_entry["Risk_Factors"]:
            if current_entry["Risk_Factors"][factor] != "":
                current_entry["Risk_Factors"][factor] = ""
                changes_made += 1
    else:
        backup_entry = next((wa for wa in backup_data["work_areas"] if wa["Work_Area"] == triggered_area), None)
        if not backup_entry:
            # Fixed: Return no_update instead of empty lists
            return f"Error: Backup not found", change_log, no_update, no_update
        for factor, default_value in backup_entry["Risk_Factors"].items():
            if current_entry["Risk_Factors"].get(factor) != default_value:
                current_entry["Risk_Factors"][factor] = default_value
                changes_made += 1

    with open(risk_data_path, "w") as f:
        json.dump(current_data, f, indent=4)

    # Remove change log entries for this area
    filtered_log = [log for log in change_log if not log.children.startswith(triggered_area.replace('_', ' '))]
    change_log[:] = filtered_log
    change_count = len(filtered_log)

    latest = {wa["Work_Area"]: wa["Risk_Factors"] for wa in current_data["work_areas"]}
    colors, outlines = [], []
    for btn in button_ids:
        a, f_, v = btn["area"], btn["factor"], btn["value"]
        current_val = latest.get(a, {}).get(f_)
        colors.append("primary" if current_val == v else "secondary")
        outlines.append(current_val != v)

    status_msg = f"{triggered_area.replace('_', ' ')} reset {'to defaults ✅' if not is_user_created else 'to blank values ✅'}"
    return status_msg, change_log, colors, outlines

@callback(
    Output("update-status", "children", allow_duplicate=True),
    Output("change-log", "children", allow_duplicate=True),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "color", allow_duplicate=True),
    Output({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "outline", allow_duplicate=True),
    Output("change-counter", "children", allow_duplicate=True),
    Output("workstations-container", "children", allow_duplicate=True),
    Input("reset-work-areas", "n_clicks"),
    State({"type": "btn-option", "area": ALL, "factor": ALL, "value": ALL}, "id"),
    prevent_initial_call=True
)
def reset_all_work_areas(n_clicks, button_ids):
    global change_log, change_count
    
    # Handle the case where n_clicks is None or 0
    if not n_clicks:
        return no_update, no_update, no_update, no_update, no_update, no_update

    # Load backup and current data
    with open(backup_data_path, "r") as f:
        backup_data = json.load(f)
    with open(risk_data_path, "r") as f:
        current_data = json.load(f)

    # Identify default risk factors
    default_risk_factors = set(backup_data["Risk_Factors_Matrix"].keys())
    
    # Find custom risk factors that should be removed
    current_risk_factors = set(current_data["Risk_Factors_Matrix"].keys())
    custom_risk_factors_to_remove = current_risk_factors - default_risk_factors

    # 1. Reset the Risk_Factors_Matrix to default (from backup)
    current_data["Risk_Factors_Matrix"] = json.loads(json.dumps(backup_data["Risk_Factors_Matrix"]))  # deep copy
    
    # 2. Reset all work areas to the ones from the backup
    current_data["work_areas"] = json.loads(json.dumps(backup_data["work_areas"]))  # deep copy

    # Save the updated data back to the file
    with open(risk_data_path, "w") as f:
        json.dump(current_data, f, indent=4)

    # Clear the change log
    change_log.clear()
    change_count = 0

    # Update button states based on the reset data
    latest = {wa["Work_Area"]: wa["Risk_Factors"] for wa in current_data["work_areas"]}
    colors, outlines = [], []
    for btn in button_ids:
        a, f_, v = btn["area"], btn["factor"], btn["value"]
        # Skip buttons for factors that no longer exist after reset
        if f_ in custom_risk_factors_to_remove:
            continue
        current_val = latest.get(a, {}).get(f_)
        colors.append("primary" if current_val == v else "secondary")
        outlines.append(current_val != v)
    
    # Generate updated cards with the reset data
    updated_cards = get_workstation_cards()
    
    # Build status message including info about removed custom factors
    status_message = "All work areas reset ✅"
    if custom_risk_factors_to_remove:
        removed_count = len(custom_risk_factors_to_remove)
        status_message += f" {removed_count} custom risk factor{'s' if removed_count > 1 else ''} removed."
    
    return status_message, [], colors, outlines, "", updated_cards

# Fixed modal toggle and add work area workflow
@callback(
    Output("add-workarea-modal", "is_open"),
    Output("new-workarea-name", "value"),
    [Input("open-add-modal", "n_clicks"),
     Input("confirm-add-workarea", "n_clicks"),
     Input("cancel-add-modal", "n_clicks")],
    [State("add-workarea-modal", "is_open"),
     State("new-workarea-name", "value")],
    prevent_initial_call=True
)
def toggle_modal(open_click, confirm_click, cancel_click, is_open, current_name):
    triggered_id = ctx.triggered_id
    
    # Only open the modal if the "Add Work Area" button was clicked
    if triggered_id == "open-add-modal" and open_click:
        return True, ""
    
    # Close the modal if either "Add" or "Cancel" was clicked
    elif triggered_id in ["confirm-add-workarea", "cancel-add-modal"]:
        return False, ""
    
    # Default case
    return is_open, current_name

@callback(
    Output("workstations-container", "children"),
    Output("update-status", "children", allow_duplicate=True),
    Output("change-counter", "children", allow_duplicate=True),  # Fixed: Added missing output
    Input("confirm-add-workarea", "n_clicks"),
    State("new-workarea-name", "value"),
    prevent_initial_call=True
)
def add_new_work_area(n_clicks, name):
    if not n_clicks or not name:
        return no_update, "Please enter a name for the new work area.", no_update
    
    # Normalize name
    name_clean = name.strip().replace(" ", "_")

    with open(risk_data_path, "r") as f:
        data = json.load(f)

    risk_factors_matrix = data.get("Risk_Factors_Matrix", {})

    # Check if work area already exists
    if any(wa["Work_Area"].lower() == name_clean.lower() for wa in data["work_areas"]):
        return no_update, f"Work area '{name}' already exists (case-insensitive match).", no_update

    # Create new work area
    new_area = {"Work_Area": name_clean, "Risk_Factors": {k: "" for k in risk_factors_matrix}}
    data["work_areas"].append(new_area)

    # Save data
    with open(risk_data_path, "w") as f:
        json.dump(data, f, indent=4)

    # Generate the updated card rows
    updated_card_rows = get_workstation_cards()
    
    # Fixed: Added the missing output for change-counter
    return updated_card_rows, f"New work area '{name}' added ✅", ""

@callback(
    Output("workstations-container", "children", allow_duplicate=True),
    Output("update-status", "children", allow_duplicate=True),
    Input({"type": "delete-button", "area": ALL}, "n_clicks"),
    State({"type": "delete-button", "area": ALL}, "id"),
    prevent_initial_call=True
)
def delete_work_area(n_clicks, ids):
    global change_log, change_count

    if not any(n_clicks):
        return no_update, no_update

    # Identify which button was clicked
    idx = next((i for i, click in enumerate(n_clicks) if click), None)
    if idx is None:
        return no_update, no_update

    area_to_delete = ids[idx]["area"]

    # Load and modify JSON data
    data = load_json(risk_data_path)
    data["work_areas"] = [wa for wa in data["work_areas"] if wa["Work_Area"] != area_to_delete]
    save_json(risk_data_path, data)

    # 🧼 Clean up the change log for this deleted work area
    formatted_area_name = area_to_delete.replace('_', ' ')
    filtered_log = [log for log in change_log if not log.children.startswith(formatted_area_name)]
    change_log[:] = filtered_log
    change_count = len(filtered_log)

    # Update cards
    updated_cards = get_workstation_cards()
    return updated_cards, f"Work area '{formatted_area_name}' deleted ✅"


