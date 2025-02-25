from dash import html
import dash_bootstrap_components as dbc

def dashboard():
    return html.H1(f"Welcome {session_user}! You are logged in.")