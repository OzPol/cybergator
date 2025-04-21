import json, os
from dash import html, dcc, Input, Output, State, callback, ctx, ALL, no_update
import dash_bootstrap_components as dbc

# Updated to use a single file for both work areas and risk factors
DATA_PATH = os.path.join("app", "data", "json", "Risk_Factors.json")
BACKUP_DATA_PATH = os.path.join("app", "data", "backup", "Risk_Factors.json")

def load_data():
    """Load the full data structure containing both work areas and risk factors"""
    with open(DATA_PATH, "r") as f:
        data = json.load(f)
    return data

def load_risk_matrix():
    """Load just the risk factors matrix from the data file"""
    data = load_data()
    return data["Risk_Factors_Matrix"]

def environmental_factors_layout():
    risk_matrix = load_risk_matrix()
    
    # Group risk factors into rows (3 per row on large screens)
    matrix_cards = []
    for factor, levels in risk_matrix.items():
        rows = []
        for level, weight in levels.items():
            rows.append(
                dbc.Row([
                    dbc.Col(html.Span(level, className="fw-semibold"), width=6),
                    dbc.Col(
                        dbc.Input(
                            type="number",
                            value=weight,
                            min=0, max=2.0, step=0.1,
                            id={"type": "matrix-input", "factor": factor, "level": level},
                            className="w-100"
                        ),
                        width=6
                    )
                ], className="mb-2")
            )
        
        # Add remove button in the header next to the factor name
        card_header = dbc.CardHeader([
            dbc.Row([
                dbc.Col(html.H5(factor.replace("_", " ").capitalize(), className="mb-0"), width=9),
                dbc.Col(
                    dbc.Button(
                        "❌ Remove", 
                        id={"type": "remove-factor-btn", "factor": factor},
                        color="danger",
                        size="sm",
                        className="float-end"
                    ),
                    width=3,
                    className="text-end"
                )
            ])
        ])
        
        card = dbc.Card([
            card_header,
            dbc.CardBody(rows)
        ], className="h-100 shadow-sm")
        
        matrix_cards.append(card)
    
    # Create rows with 3 cards each
    matrix_rows = []
    for i in range(0, len(matrix_cards), 3):
        row_cards = matrix_cards[i:i+3]
        cols = []
        for card in row_cards:
            cols.append(dbc.Col(card, width=12, md=4, className="mb-4"))
        
        # If this is the last row and there are fewer than 3 cards, add empty columns to maintain grid
        while len(cols) < 3:
            cols.append(dbc.Col(width=12, md=4, className="mb-4"))
            
        row = dbc.Row(cols, className="g-3")
        matrix_rows.append(row)

    # Create inline "Add Risk Factor" section
    add_risk_factor_section = dbc.Card([
        dbc.CardHeader(html.H5("Add a New Risk Factor", className="mb-0")),
        dbc.CardBody([
            # Error alert that will show validation errors
            html.Div(id="new-factor-validation-alert"),
            
            dbc.Row([
                # Risk Factor Name
                dbc.Col([
                    dbc.Label("Risk Factor Name"),
                    dbc.Input(id="new-risk-factor-name", placeholder="Enter name")
                ], width=12, md=3),
                
                # Option Type
                dbc.Col([
                    dbc.Label("Option Type"),
                    dbc.Select(
                        id="risk-factor-option-type",
                        options=[
                            {"label": "Yes/No/NA", "value": "yes_no"},
                            {"label": "Low/Medium/High/NA", "value": "low_high"},
                            {"label": "None/Limited/Full/NA", "value": "none_full"},
                            {"label": "Part-time/Full-time/No/NA", "value": "employment"}
                        ]
                    )
                ], width=12, md=3),
                
                # Default Value
                dbc.Col([
                    dbc.Label("Default Value"),
                    dbc.Select(
                        id="default-work-area-value",
                        options=[]  # Will be populated based on selected option type
                    )
                ], width=12, md=3),
                
                # Add Button
                dbc.Col([
                    dbc.Label("\u00A0"),  # Non-breaking space to align with inputs
                    dbc.Button(
                        "➕ Add Risk Factor", 
                        id="add-risk-factor-btn", 
                        color="success", 
                        className="w-100"
                    )
                ], width=12, md=3)
            ]),
            
            # Weight inputs will appear below when an option type is selected
            html.Div(id="weight-inputs-container", className="mt-3")
        ])
    ], className="mb-4 shadow-sm")

    return dbc.Container([
        dcc.Store(id="add-success-flag", data=False),

        dbc.Row([
            dbc.Col([
                html.H2("Edit Environmental Risk Factor Weights", className="text-center mt-4 mb-3"),
                html.P("Adjust the impact weight of each risk factor value on resilience scoring (0-2.0).", 
                       className="text-center"),
                html.Hr(),
            ], width=12)
        ]),
        html.Div(matrix_rows, id="risk-matrix-container", className="mb-4"),
        add_risk_factor_section,
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        dbc.Button("💾 Save Changes", id="save-matrix-btn", color="primary", className="w-100"),
                        width=12, md=6, className="mb-2 mb-md-0"
                    ),
                    dbc.Col(
                        dbc.Button("🔄 Reset to Default", id="reset-matrix-btn", color="secondary", className="w-100"),
                        width=12, md=6
                    )
                ]),
                html.Div(id="save-status", className="mt-3 text-center")
            ], width=12, lg=6, className="mx-auto")
        ])
    ], fluid=True)

@callback(
    [Output("risk-matrix-container", "children", allow_duplicate=True),
     Output("save-status", "children", allow_duplicate=True)],
    Input({"type": "remove-factor-btn", "factor": ALL}, "n_clicks"),
    State({"type": "remove-factor-btn", "factor": ALL}, "id"),
    prevent_initial_call=True
)
def remove_risk_factor(n_clicks_list, btn_ids):
    if not any(n_clicks for n_clicks in n_clicks_list if n_clicks):
        return no_update, no_update

    # Determine which button was clicked
    triggered_idx = next((i for i, n in enumerate(n_clicks_list) if n), None)
    if triggered_idx is None:
        return no_update, no_update

    factor_to_remove = btn_ids[triggered_idx]["factor"]
    factor_display_name = factor_to_remove.replace("_", " ").capitalize()

    try:
        data = load_data()

        # Remove the risk factor from the matrix
        if factor_to_remove in data["Risk_Factors_Matrix"]:
            del data["Risk_Factors_Matrix"][factor_to_remove]

        # Remove from all work areas
        for work_area in data.get("work_areas", []):
            if factor_to_remove in work_area.get("Risk_Factors", {}):
                del work_area["Risk_Factors"][factor_to_remove]

        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)

        # Rebuild matrix display
        risk_matrix = data["Risk_Factors_Matrix"]
        matrix_cards = []
        for factor, levels in risk_matrix.items():
            rows = []
            for level, weight in levels.items():
                rows.append(
                    dbc.Row([
                        dbc.Col(html.Span(level, className="fw-semibold"), width=6),
                        dbc.Col(
                            dbc.Input(
                                type="number",
                                value=weight,
                                min=0, max=2.0, step=0.1,
                                id={"type": "matrix-input", "factor": factor, "level": level},
                                className="w-100"
                            ),
                            width=6
                        )
                    ], className="mb-2")
                )

            card_header = dbc.CardHeader([
                dbc.Row([
                    dbc.Col(html.H5(factor.replace("_", " ").capitalize(), className="mb-0"), width=9),
                    dbc.Col(
                        dbc.Button(
                            "❌ Remove",
                            id={"type": "remove-factor-btn", "factor": factor},
                            color="danger",
                            size="sm",
                            className="float-end"
                        ),
                        width=3,
                        className="text-end"
                    )
                ])
            ])

            card = dbc.Card([card_header, dbc.CardBody(rows)], className="h-100 shadow-sm")
            matrix_cards.append(card)

        # Organize into rows of 3
        matrix_rows = []
        for i in range(0, len(matrix_cards), 3):
            row_cards = matrix_cards[i:i+3]
            cols = [dbc.Col(card, width=12, md=4, className="mb-4") for card in row_cards]
            while len(cols) < 3:
                cols.append(dbc.Col(width=12, md=4, className="mb-4"))
            matrix_rows.append(dbc.Row(cols, className="g-3"))

        return matrix_rows, html.Div(f"✅ Risk factor '{factor_display_name}' removed from all work areas.", className="text-success")

    except Exception as e:
        return no_update, html.Div(f"Error removing risk factor: {e}", className="text-danger")

@callback(
    [Output("weight-inputs-container", "children"),
     Output("default-work-area-value", "options"),
     Output("default-work-area-value", "value")],
    Input("risk-factor-option-type", "value"),
    prevent_initial_call=True
)
def update_weight_inputs(option_type):
    if not option_type:
        return [], [], None
    
    # Define options based on the selected type
    options_map = {
        "yes_no": ["Yes", "No", "NA"],
        "low_high": ["Low", "Medium", "High", "NA"],
        "none_full": ["None", "Limited", "Full", "NA"],
        "employment": ["Part-time", "Full-time", "No", "NA"]
    }
    
    options = options_map.get(option_type, [])
    
    # Create input fields for each option's weight value in a horizontal layout
    weight_inputs = []
    
    # Create row for weight input labels
    weight_labels = []
    for option in options:
        weight_labels.append(
            dbc.Col(
                html.Label(f"Weight for '{option}'"),
                width=12, md=len(options) and (12 // len(options))
            )
        )
    
    # Create row for weight input fields
    weight_fields = []
    for option in options:
        default_value = 1.0 if option not in ["NA", "No"] else 0.0
        weight_fields.append(
            dbc.Col(
                dbc.Input(
                    type="number",
                    value=default_value,
                    min=0, max=2.0, step=0.1,
                    id={"type": "option-weight", "option": option}
                ),
                width=12, md=len(options) and (12 // len(options))
            )
        )
    
    weight_inputs = [
        dbc.Row(weight_labels, className="mb-2"),
        dbc.Row(weight_fields),
        dbc.Row(
            dbc.Col(
                dbc.FormText("Values must be between 0 and 2.0"),
                className="mt-1"
            )
        )
    ]
    
    # Create options for default value dropdown
    default_options = [{"label": opt, "value": opt} for opt in options]
    
    # Set a reasonable default value for the dropdown
    default_value = options[0] if options else None
    
    return html.Div(weight_inputs), default_options, default_value

@callback(
    Output("new-factor-validation-alert", "children"),
    [Input("add-risk-factor-btn", "n_clicks"),
     Input("risk-factor-option-type", "value")],
    [State("new-risk-factor-name", "value"),
     State({"type": "option-weight", "option": ALL}, "id"),
     State({"type": "option-weight", "option": ALL}, "value"),
     State("risk-factor-option-type", "value"),
     State("add-success-flag", "data")],
    prevent_initial_call=True
)
def validate_new_factor(n_clicks, option_type_trigger, factor_name, option_ids, option_weights, option_type_state, success_flag):
    if ctx.triggered_id == "risk-factor-option-type":
        return None

    if not n_clicks or ctx.triggered_id != "add-risk-factor-btn":
        return None

    if success_flag:
        return None

    validation_errors = []

    if not factor_name or not factor_name.strip():
        validation_errors.append("Risk factor name is required")

    if not option_type_state:
        validation_errors.append("Option type must be selected")

    for i, weight in enumerate(option_weights):
        option = option_ids[i]["option"]
        if weight is None:
            validation_errors.append(f"Weight for '{option}' must be between 0 and 2.0")

    if validation_errors:
        error_items = [html.Li(error) for error in validation_errors]
        return dbc.Alert(
            [html.H6("Please fix the following errors:"), html.Ul(error_items)],
            color="danger", className="mb-3"
        )

    return None

@callback(
    [Output("risk-matrix-container", "children"),
     Output("save-status", "children"),
     Output("new-factor-validation-alert", "children", allow_duplicate=True),
     Output("new-risk-factor-name", "value"),
     Output("risk-factor-option-type", "value"),
     Output("add-success-flag", "data")],
    Input("add-risk-factor-btn", "n_clicks"),
    [State("new-risk-factor-name", "value"),
     State("risk-factor-option-type", "value"),
     State({"type": "option-weight", "option": ALL}, "id"),
     State({"type": "option-weight", "option": ALL}, "value"),
     State("default-work-area-value", "value")],
    prevent_initial_call=True
)
def add_new_risk_factor(n_clicks, factor_name, option_type, option_ids, option_weights, default_value):
    if not n_clicks:
        return no_update, no_update, no_update, no_update, no_update, False

    factor_key = factor_name.strip().replace(" ", "_").lower()

    try:
        options_map = {
            "yes_no": ["Yes", "No", "NA"],
            "low_high": ["Low", "Medium", "High", "NA"],
            "none_full": ["None", "Limited", "Full", "NA"],
            "employment": ["Part-time", "Full-time", "No", "NA"]
        }
        options = options_map.get(option_type, [])

        # FULL validation logic here
        validation_errors = []
        if not factor_name or not factor_name.strip():
            validation_errors.append("Risk factor name is required")

        if not option_type:
            validation_errors.append("Option type must be selected")

        for i, weight in enumerate(option_weights):
            option = option_ids[i]["option"]
            if weight is None or not (0 <= weight <= 2.0):
                validation_errors.append(f"Weight for '{option}' must be between 0 and 2.0.")

        if validation_errors:
            return (
                no_update,
                no_update,
                dbc.Alert([
                    html.H6("Please fix the following errors:"),
                    html.Ul([html.Li(msg) for msg in validation_errors])
                ], color="danger", className="mb-3"),
                no_update,
                no_update,
                False
            )

        data = load_data()

        if factor_key in data["Risk_Factors_Matrix"]:
            error_msg = f"Risk factor '{factor_name}' already exists!"
            return no_update, no_update, dbc.Alert(error_msg, color="danger", className="mb-3"), no_update, no_update, False

        weights = {option_ids[i]["option"]: option_weights[i] for i in range(len(option_ids))}
        data["Risk_Factors_Matrix"][factor_key] = weights

        for work_area in data["work_areas"]:
            work_area["Risk_Factors"][factor_key] = default_value

        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)

        risk_matrix = data["Risk_Factors_Matrix"]

        matrix_cards = []
        for factor, levels in risk_matrix.items():
            rows = [
                dbc.Row([
                    dbc.Col(html.Span(level, className="fw-semibold"), width=6),
                    dbc.Col(
                        dbc.Input(
                            type="number",
                            value=weight,
                            min=0, max=2.0, step=0.1,
                            id={"type": "matrix-input", "factor": factor, "level": level},
                            className="w-100"
                        ),
                        width=6
                    )
                ], className="mb-2")
                for level, weight in levels.items()
            ]

            # Add remove button in the header
            card_header = dbc.CardHeader([
                dbc.Row([
                    dbc.Col(html.H5(factor.replace("_", " ").capitalize(), className="mb-0"), width=9),
                    dbc.Col(
                        dbc.Button(
                            "❌ Remove", 
                            id={"type": "remove-factor-btn", "factor": factor},
                            color="danger",
                            size="sm",
                            className="float-end"
                        ),
                        width=3,
                        className="text-end"
                    )
                ])
            ])

            matrix_cards.append(dbc.Card([
                card_header,
                dbc.CardBody(rows)
            ], className="h-100 shadow-sm"))

        matrix_rows = []
        for i in range(0, len(matrix_cards), 3):
            row_cards = matrix_cards[i:i+3]
            cols = [dbc.Col(card, width=12, md=4, className="mb-4") for card in row_cards]
            while len(cols) < 3:
                cols.append(dbc.Col(width=12, md=4, className="mb-4"))
            matrix_rows.append(dbc.Row(cols, className="g-3"))

        return (
            matrix_rows,
            html.Div(f"✅ Successfully added new risk factor '{factor_name}'!", className="text-success"),
            None,
            "",  # Clear name
            "",  # Clear option type
            True  # Set success flag
        )

    except Exception as e:
        return no_update, no_update, dbc.Alert(f"Error: {e}", color="danger"), no_update, no_update, False

    
@callback(
    Output("save-status", "children", allow_duplicate=True),
    Input("save-matrix-btn", "n_clicks"),
    State({"type": "matrix-input", "factor": ALL, "level": ALL}, "id"),
    State({"type": "matrix-input", "factor": ALL, "level": ALL}, "value"),
    prevent_initial_call=True
)
def save_updated_matrix(n_clicks, ids, values):
    if not ids or not values:
        return "Nothing to save."
    
    try:
        # Load the current data
        with open(DATA_PATH, "r") as f:
            data = json.load(f)
        
        # Get original values for comparison
        original_values = {}
        for factor, levels in data["Risk_Factors_Matrix"].items():
            for level, weight in levels.items():
                original_values[(factor, level)] = weight
        
        # Track changes and validate
        validation_errors = []
        changed_fields = []
        
        for i, id_pair in enumerate(ids):
            factor = id_pair["factor"]
            level = id_pair["level"]
            new_value = values[i]
            original = original_values.get((factor, level))
            
            # Only validate if the value was actually changed
            if new_value != original:
                changed_fields.append((factor, level, new_value))
                
                # Validate the changed value
                if new_value is None or not (0 <= new_value <= 2.0):
                    validation_errors.append(f"'{factor} → {level}' must be between 0 and 2.0")
        
        # If there are validation errors, show them
        if validation_errors:
            error_display = html.Div([
                html.Div(error) for error in validation_errors
            ])
            return html.Div([
                html.Div("❌ Invalid values detected:", className="text-danger fw-bold"),
                error_display
            ])
        
        # If no errors, save changes
        if changed_fields:
            for factor, level, new_value in changed_fields:
                data["Risk_Factors_Matrix"][factor][level] = new_value
                
            with open(DATA_PATH, "w") as f:
                json.dump(data, f, indent=4)
                
            num_changes = len(changed_fields)
            return html.Div(f"✅ Successfully saved {num_changes} change{'s' if num_changes > 1 else ''}!", 
                           className="text-success")
        else:
            return "No changes detected."
    
    except Exception as e:
        return html.Div(f"Error saving data: {e}", className="text-danger")

@callback(
    Output("risk-matrix-container", "children", allow_duplicate=True),
    Output("save-status", "children", allow_duplicate=True),
    Input("reset-matrix-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_matrix_to_default(n_clicks):
    if not n_clicks:
        return no_update, no_update
    
    try:
        # Load default values from backup
        with open(BACKUP_DATA_PATH, "r") as f:
            backup_data = json.load(f)
        
        # Load current data structure
        with open(DATA_PATH, "r") as f:
            current_data = json.load(f)
        
        # Get the list of risk factors that should be kept (those in the default/backup data)
        default_risk_factors = set(backup_data["Risk_Factors_Matrix"].keys())
        
        # Find custom risk factors that should be removed
        current_risk_factors = set(current_data["Risk_Factors_Matrix"].keys())
        custom_risk_factors_to_remove = current_risk_factors - default_risk_factors
        
        # Replace current risk factors with backup values
        current_data["Risk_Factors_Matrix"] = backup_data["Risk_Factors_Matrix"]
        
        # Clean up custom risk factors and restore default ones with original values
        for work_area in current_data["work_areas"]:
            # Remove custom factors
            for factor_to_remove in custom_risk_factors_to_remove:
                work_area["Risk_Factors"].pop(factor_to_remove, None)

            # Build a mapping of original work area defaults from the backup
            original_work_areas = {
                wa["Work_Area"]: wa["Risk_Factors"]
                for wa in backup_data.get("work_areas", [])
            }

            for work_area in current_data["work_areas"]:
                work_area_name = work_area.get("Work_Area")
                
                # Remove any custom risk factors
                for factor_to_remove in custom_risk_factors_to_remove:
                    work_area["Risk_Factors"].pop(factor_to_remove, None)

                # Restore default risk factors with the original selected value from the backup
                default_risk_values = original_work_areas.get(work_area_name, {})
                for factor_key in backup_data["Risk_Factors_Matrix"]:
                    if factor_key in default_risk_values:
                        work_area["Risk_Factors"][factor_key] = default_risk_values[factor_key]
                    else:
                        # Fallback: assign "NA" if not found
                        work_area["Risk_Factors"][factor_key] = "NA"


        
        # Save the updated data
        with open(DATA_PATH, "w") as f:
            json.dump(current_data, f, indent=4)
        
        # Rebuild the matrix inputs with the default values in grid layout
        risk_matrix = backup_data["Risk_Factors_Matrix"]
        
        # Create cards for each factor
        matrix_cards = []
        for factor, levels in risk_matrix.items():
            rows = []
            for level, weight in levels.items():
                rows.append(
                    dbc.Row([
                        dbc.Col(html.Span(level, className="fw-semibold"), width=6),
                        dbc.Col(
                            dbc.Input(
                                type="number",
                                value=weight,
                                min=0, max=2.0, step=0.1,
                                id={"type": "matrix-input", "factor": factor, "level": level},
                                className="w-100"
                            ),
                            width=6
                        )
                    ], className="mb-2")
                )
            
            # Add remove button in the header
            card_header = dbc.CardHeader([
                dbc.Row([
                    dbc.Col(html.H5(factor.replace("_", " ").capitalize(), className="mb-0"), width=9),
                    dbc.Col(
                        dbc.Button(
                            "❌ Remove", 
                            id={"type": "remove-factor-btn", "factor": factor},
                            color="danger",
                            size="sm",
                            className="float-end"
                        ),
                        width=3,
                        className="text-end"
                    )
                ])
            ])
            
            card = dbc.Card([
                card_header,
                dbc.CardBody(rows)
            ], className="h-100 shadow-sm")
            
            matrix_cards.append(card)
        
        # Create rows with 3 cards each
        matrix_rows = []
        for i in range(0, len(matrix_cards), 3):
            row_cards = matrix_cards[i:i+3]
            cols = []
            for card in row_cards:
                cols.append(dbc.Col(card, width=12, md=4, className="mb-4"))
            
            # If this is the last row and there are fewer than 3 cards, add empty columns to maintain grid
            while len(cols) < 3:
                cols.append(dbc.Col(width=12, md=4, className="mb-4"))
                
            row = dbc.Row(cols, className="g-3")
            matrix_rows.append(row)
        
        # Calculate how many custom risk factors were removed
        removed_count = len(custom_risk_factors_to_remove)
        success_message = "✅ Risk factors reset to default values!"
        if removed_count > 0:
            success_message += f" {removed_count} custom risk factor{'s' if removed_count > 1 else ''} removed."
        
        return matrix_rows, html.Div(success_message, className="text-success")
    
    except Exception as e:
        return no_update, html.Div(f"Error resetting data: {e}", className="text-danger")