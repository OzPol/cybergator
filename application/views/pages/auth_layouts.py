from dash import dcc, html
import dash_bootstrap_components as dbc


def get_auth_layout():
    return dbc.Container([
        dcc.Location(id="redirect", refresh=True),
    dbc.Row(dbc.Col(html.H1("Login/Register Page", className="text-center mt-4"))),
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Label("Username:", className="font-weight-bold"),
                        dbc.Input(type="text", id="username", placeholder="Enter your username", className="mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Label("Password:", className="font-weight-bold"),
                        dbc.Input(type="password", id="password", placeholder="Enter your password", className="mb-3"),
                    ]),
                    dbc.Button("Login", id="login-btn", color="primary", className="w-100 mb-3"),
                    dbc.Button("Register", id="signup-btn", color="success", className="w-100 mb-3"),
                    html.Div(id="auth-output", className="text-center"),  # To display login success/error messages
                    dcc.Link('Go back to Homepage', href='/welcome', className="btn btn-link d-block text-center"),
                ]),
            ]),
        ], className="shadow p-3 mb-5 bg-white rounded", style={"maxWidth": "400px", "margin": "auto"}),
    )),
], fluid=True, className="d-flex flex-column justify-content-start align-items-center vh-100 mt-5")
