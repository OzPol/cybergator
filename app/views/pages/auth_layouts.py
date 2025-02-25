from dash import dcc, html
import dash_bootstrap_components as dbc


def get_auth_layout():
    return dbc.Container([
    dbc.Row(dbc.Col(html.H1("Login Page", className="text-center mt-4"))),
    dbc.Row(dbc.Col(
        dbc.Card([
            dbc.CardBody([
                dbc.Form([
                    dbc.Row([
                        dbc.Label("Username:", className="font-weight-bold"),
                        dbc.Input(type="text", id="login-username", placeholder="Enter your username", className="mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Label("Password:", className="font-weight-bold"),
                        dbc.Input(type="password", id="login-password", placeholder="Enter your password", className="mb-3"),
                    ]),
                    dbc.Button("Login", id="login-button", color="primary", className="w-100 mb-3"),
                    html.Div(id="login-message", className="text-center"),  # To display login success/error messages
                    dcc.Link('Go back to Homepage', href='/welcome', className="btn btn-link d-block text-center"),
                ]),
            ]),
        ], className="shadow p-3 mb-5 bg-white rounded", style={"maxWidth": "400px", "margin": "auto"}),
    )),
], fluid=True, className="d-flex flex-column justify-content-start align-items-center vh-100 mt-5")
