from dash import dcc, html

def get_auth_layout():
    return html.Div([
        dcc.Location(id="redirect", refresh=True),  # Redirect without full reload
        html.H2("Login / Signup"),
        dcc.Input(id="username", type="text", placeholder="Username"),
        dcc.Input(id="password", type="password", placeholder="Password"),
        html.Button("Login", id="login-btn", n_clicks=0),
        html.Button("Sign Up", id="signup-btn", n_clicks=0),
        html.Div(id="auth-output")
    ])
