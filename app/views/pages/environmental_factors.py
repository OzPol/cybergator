import json, os
from dash import html, dcc, Input, Output, State, callback, ctx, ALL
import dash_bootstrap_components as dbc

RISK_FACTORS_PATH = os.path.join("app", "data", "json", "Risk_Factors.json")

def load_risk_matrix():
    with open(RISK_FACTORS_PATH, "r") as f:
        data = json.load(f)
    return data["Risk_Factors_Matrix"]

def environmental_factors_layout():
    risk_matrix = load_risk_matrix()

    matrix_inputs = []
    for factor, levels in risk_matrix.items():
        rows = []
        for level, weight in levels.items():
            rows.append(
                dbc.Row([
                    dbc.Col(html.Span(level, className="text-end fw-semibold"), width=4),
                    dbc.Col(
                        dbc.Input(
                            type="number",
                            value=weight,
                            min=0, step=0.1,
                            id={"type": "matrix-input", "factor": factor, "level": level},
                            className="w-100"
                        ),
                        width=4
                    )
                ], className="mb-2", justify="center")
            )
        matrix_inputs.append(
            dbc.Card([
                dbc.CardHeader(html.H5(factor.replace("_", " ").capitalize(), className="mb-0")),
                dbc.CardBody(rows)
            ], className="mb-4 shadow-sm")
        )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Edit Environmental Risk Factor Weights", className="text-center mt-4 mb-3"),
                html.P("Adjust the impact weight of each risk factor value on resilience scoring.", className="text-center"),
                html.Hr(),
                html.Div(matrix_inputs, id="risk-matrix-container"),
                dbc.Button("💾 Save Changes", id="save-matrix-btn", color="primary", className="mt-3"),
                html.Div(id="save-status", className="text-success mt-3 text-center")
            ], width=12, lg=8, className="offset-lg-2")
        ])
    ], fluid=True)

@callback(
    Output("save-status", "children"),
    Input("save-matrix-btn", "n_clicks"),
    State({"type": "matrix-input", "factor": ALL, "level": ALL}, "id"),
    State({"type": "matrix-input", "factor": ALL, "level": ALL}, "value"),
    prevent_initial_call=True
)
def save_updated_matrix(n_clicks, ids, values):
    if not ids or not values:
        return "Nothing to save."
    
    try:
        with open(RISK_FACTORS_PATH, "r") as f:
            data = json.load(f)
        
        # Update weights
        for i, id_pair in enumerate(ids):
            factor = id_pair["factor"]
            level = id_pair["level"]
            new_value = values[i]
            data["Risk_Factors_Matrix"][factor][level] = new_value

        with open(RISK_FACTORS_PATH, "w") as f:
            json.dump(data, f, indent=4)

        return "Changes saved successfully ✅"
    
    except Exception as e:
        return f"Error saving data: {e}"
