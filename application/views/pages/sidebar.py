from dash import html
import dash_bootstrap_components as dbc

def sidebar():
    return html.Div(
        [
            html.H2("Menu", className="display-4", style={"color": "white", "textAlign": "center"}),
            html.Hr(style={"borderTop": "1px solid white"}),

            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/welcome", active="exact", style={"color": "white"}),
                    dbc.NavLink("Login/Register", href="/auth", active="exact", style={"color": "white"}),
                    dbc.NavLink("Dashboard", href="/dashboard", active="exact", style={"color": "white"}),
                ],
                vertical=True,
                pills=True,
                style={"marginTop": "20px"},
            ),
        ],
        className="sidebar"
    )
