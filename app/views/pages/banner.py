from dash import html
import dash_bootstrap_components as dbc

def banner(page_title="CyberGators", session_user=None, resilience_score=None):
    return html.Div([
        dbc.Row([
            # Left spacer to balance centering
            dbc.Col(width=1),  # Ensures the title is centered

            # Centered Page Title
            dbc.Col(
                html.H1(page_title, className="banner-title"),
                width=10,
                style={"textAlign": "center", "flexGrow": 1}  # Keep title centered
            ),

            # Right Column for Resilience Score
            dbc.Col(
                html.Div(
                    f"Resilience Score: {resilience_score}" if resilience_score else "Resilience Score: N/A",
                    id="system-resilience-score",
                    className="resilience-score-text"
                ),
                width=2,
                className="resilience-score-col"  # Apply custom CSS class here
            ),

            # Right Column for Logout Button
            dbc.Col(
                dbc.Button("Logout", id="logout-btn", n_clicks=0, className="logout-button", color="primary"),
                width=1, 
                style={"textAlign": "center", "paddingRight": "0px", "position": "absolute", "right": "0px", "top": "25px"}
            ) if session_user else None
        ], align="center", justify="between", className="banner-row"),
    ], className="banner")
