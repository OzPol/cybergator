from dash import html, dcc
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
            dbc.NavLink("CVE Simulation", href="/cve-simulation", active="exact", style={"color": "white"}),
            dbc.NavLink("FSM Simulation", href="/fsm-simulation", active="exact", style={"color": "white"}),
            dbc.NavLink("Neo4j Graph", href="/neo4j-graph", active="exact", style={"color": "white"}),
        ]
        # Append extra links to the nav_items list
        nav_items.extend(extra_links)
        
        # RECALCULATE RESILIENCE BUTTON
        nav_items.append(
            html.Div([
                dbc.Button("Recalculate Resilience", id="recalculate-resilience-btn", color="primary",
                        className="mt-2", style={"width": "100%"}),
                html.Div(id="resilience-recalculate-feedback", className="text-white mt-2", style={"fontSize": "0.9rem"})
            ], style={"position": "absolute", "bottom": "190px", "width": "80%"})
        )

        # Hidden div for triggering resilience score updates
        nav_items.append(
            html.Div(id="resilience-update-trigger", style={"display": "none"})
        )
        
        # Timer to auto-clear the feedback message
        nav_items.append(
            dcc.Interval(id="resilience-feedback-clear-timer", interval=4000, n_intervals=0, disabled=True)
        )

        # REFRESH NEO4J GRAPH BUTTON
        nav_items.append(
            dbc.Button("Refresh Neo4j Graph", id="refresh-neo4j-btn", color="primary",
                        className="mt-2", style={"position": "absolute", "bottom": "110px", "width": "80%"})
        )

        # EXPORT DATA BUTTON
        nav_items.append(
            dbc.Button("Export Data", id="export-btn", color="primary", href="/export", style={"position": "absolute", "bottom": "40px", "width": "80%"})
        )
        
        # RESET OPTIONS
        nav_items.append(
            dbc.DropdownMenu(
                label="Reset Options",
                children=[
                    dbc.DropdownMenuItem("Reset All", id="reset-all", n_clicks=0),
                    dbc.DropdownMenuItem("Reset Nodes", id="reset-nodes", n_clicks=0),
                    dbc.DropdownMenuItem("Reset Software Inventory", id="reset-software", n_clicks=0),
                    dbc.DropdownMenuItem("Reset Attack Tree", id="reset-attack", n_clicks=0),
                    dbc.DropdownMenuItem("Reset Risk Factors", id="reset-risk", n_clicks=0),
                    dbc.DropdownMenuItem("Reset Work Areas", id="reset-work-areas", n_clicks=0),
                ],
                color="primary", className="mt-2", style={"position": "absolute", "bottom": "280px","width": "100%"}
            )
        )

        # Inside your sidebar or main layout, add this Location component
        nav_items.append(dcc.Location(id="url-refresh", refresh=True))  # This will trigger the refresh

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
        ], className="sidebar",
    )
