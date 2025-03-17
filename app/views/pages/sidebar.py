from dash import html
import dash_bootstrap_components as dbc

def sidebar(session_user=None):
    # Basic menu items
    nav_items = [
        dbc.NavLink("Home", href="/welcome", active="exact", style={"color": "white"}),
        dbc.NavLink("Dashboard", href="/dashboard", active="exact", style={"color": "white"}),
    ]

    # Only add the Login/Register button if the user is not logged in
    if not session_user:
        nav_items.append(dbc.NavLink("Login/Register", href="/auth", active="exact", style={"color": "white"}))
    
    # If session_user exists, add the extra links
    if session_user:        
        extra_links = [
            dbc.NavLink("System Tables", href="/system-tables", active="exact", style={"color": "white"}),
            dbc.NavLink("System Graph", href="/system-graph", active="exact", style={"color": "white"}),
            dbc.NavLink("Environmental Factors", href="/environmental-factors", active="exact", style={"color": "white"}),
            dbc.NavLink("Work Stations", href="/work-stations", active="exact", style={"color": "white"}),
            dbc.NavLink("APT Simulation", href="/apt-simulation", active="exact", style={"color": "white"}),
            dbc.NavLink("CVE Simulations", href="/cve-simulations", active="exact", style={"color": "white"}),
            dbc.NavLink("FSM Simulation", href="/fsm-simulation", active="exact", style={"color": "white"}),
        ]
        # Append extra links to the nav_items list
        nav_items.extend(extra_links)

    return html.Div(
        [
            html.H2("Menu", className="display-4", style={"color": "white", "textAlign": "center"}),
            html.Hr(style={"borderTop": "1px solid white"}),
            dbc.Nav(
                nav_items,
                vertical=True,
                pills=True,
                style={"marginTop": "20px"},
            ),
        ],
        style={
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "15%",
            "padding": "20px",
            "backgroundColor": "blue",
            "display": "flex",
            "flexDirection": "column",
        },
    )
