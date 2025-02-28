from dash import html
import dash_bootstrap_components as dbc

def dashboard(session_user):
    return html.Div(
        html.H1(f"Welcome {session_user}! You are logged in."),
        id="page-content",
        style={
            "marginLeft": "15%",  # To account for the sidebar width
            "marginTop": "80px",   # To account for the fixed banner height
            "padding": "20px",     # Adds spacing around the content
        },
    )
