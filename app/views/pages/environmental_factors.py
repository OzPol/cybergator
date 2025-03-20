from dash import html, dcc, Input, Output, State, callback, ctx, ALL, MATCH
import dash_bootstrap_components as dbc

# Store risk factors and their values
risk_factors = [0, 1, 2, 3, 4]  # Start with 5 default factors
slider_values = {i: 50 for i in risk_factors}  # Initialize with default values

def create_risk_factor(index, value=50):
    """Generate a single risk factor row with preserved value"""
    return dbc.Row([
        dbc.Col(html.Div(f"Risk Factor #{index + 1}", className="risk-factor-title"), width=3),

        # Slider & Value (Centered Below)
        dbc.Col([
            dcc.Slider(
                id={"type": "risk-slider", "index": index},
                min=0, max=100, step=1, value=value, marks={0: "0", 100: "100"}
            ),
            html.Div(f"Value: {value}", id={"type": "slider-value", "index": index}, className="slider-value-text text-center"),  
        ], width=6, className="text-center"),

        # Remove Button
        dbc.Col(html.Button("❌", id={"type": "remove-factor", "index": index}, n_clicks=0, className="remove-btn"), width=2),

        # Description
        dbc.Col(html.P("Description", className="risk-factor-description"), width=12),
    ], className="mb-3 risk-factor-row", id=f"risk-factor-{index}")

def environmental_factors_layout():
    """Defines the Environmental Factors page layout"""
    return dbc.Container([
        html.H2("Environmental Risk Factors", className="section-title"),
        html.P("Add/Remove/Change Impact of Environmental Risk Factors", className="section-subtitle"),
        html.P(
            "This section gives a brief explanation to why we considered Env Risks, and allows a user to "
            "change their impact level/add new ones",
            className="description-text"
        ),

        # Store for slider values (hidden component)
        dcc.Store(id="slider-values-store", data=slider_values),

        # Risk Factor List (Dynamic)
        dbc.Row([
            dbc.Col(html.Div([
                html.H5("Risk Factors", className="risk-title"),
                html.Div(id="risk-factors-container", children=[create_risk_factor(i, slider_values.get(i, 50)) for i in risk_factors]),  
                dbc.Button("Add Factor", id="add-factor-btn", color="dark", className="add-factor-btn mt-3")
            ]), width=12)
        ], className="full-width-row")
    ], fluid=True, className="full-page-container")

# Callback to update the stored slider values
@callback(
    Output("slider-values-store", "data"),
    Input({"type": "risk-slider", "index": ALL}, "value"),
    State({"type": "risk-slider", "index": ALL}, "id"),
    State("slider-values-store", "data")
)
def update_slider_values(values, ids, current_data):
    """Store updated slider values"""
    for i, value in enumerate(values):
        index = ids[i]["index"]
        current_data[str(index)] = value  # Convert index to string for JSON storage
    return current_data

@callback(
    Output("risk-factors-container", "children"),
    [Input("add-factor-btn", "n_clicks"),
     Input({"type": "remove-factor", "index": ALL}, "n_clicks")],
    [State("risk-factors-container", "children"),
     State("slider-values-store", "data")],
    prevent_initial_call=True
)
def update_risk_factors(add_clicks, remove_clicks, current_factors, stored_values):
    """Handles adding and removing risk factors dynamically while preserving values."""
    global risk_factors
    global slider_values

    # Update slider_values from stored_values
    for k, v in stored_values.items():
        try:
            slider_values[int(k)] = v  # Convert string key back to integer
        except (ValueError, KeyError):
            pass  # Handle potential conversion errors

    triggered_id = ctx.triggered_id  

    if triggered_id == "add-factor-btn":
        new_index = max(risk_factors) + 1 if risk_factors else 0  
        risk_factors.append(new_index)
        slider_values[new_index] = 50  # Set default value for new slider

    elif isinstance(triggered_id, dict) and triggered_id.get("type") == "remove-factor":
        index_to_remove = triggered_id["index"]
        risk_factors = [i for i in risk_factors if i != index_to_remove]  
        risk_factors.sort()
        # Remove the value from slider_values (optional cleanup)
        if index_to_remove in slider_values:
            del slider_values[index_to_remove]

    # Use the preserved values when recreating the components
    return [create_risk_factor(i, slider_values.get(i, 50)) for i in risk_factors]

# Callback to update slider values display
@callback(
    Output({"type": "slider-value", "index": MATCH}, "children"),
    Input({"type": "risk-slider", "index": MATCH}, "value")
)
def update_slider_value(value):
    return f"Value: {value}"