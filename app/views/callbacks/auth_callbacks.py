from dash import Input, Output, State, callback, dcc, no_update, callback_context
import requests
from app.services import auth_service
from app.views.pages.auth_layouts import get_auth_layout
#from app.views.pages.register import register_layout


API_BASE_URL = "http://localhost:8000/api/auth"

@callback(
    [
        Output("auth-output", "children"),
        Output("session-user", "data"),  
        Output("redirect", "href"),
    ],
    [
        Input("login-btn", "n_clicks"),
        Input("signup-btn", "n_clicks"),
    ],
    [
        State("username", "value"),
        State("password", "value"),
    ],
    prevent_initial_call=True
)
def handle_auth(login_clicks, signup_clicks, username, password):
    ctx = callback_context
    if not username or not password:
        return "Username and password are required.", no_update, no_update

    if ctx.triggered_id == "login-btn":
        url = f"{API_BASE_URL}/login"
    elif ctx.triggered_id == "signup-btn":
        url = f"{API_BASE_URL}/signup"
    else:
        return "Unknown action.", no_update, no_update

    # Make API request
    try:
        response = requests.post(url, json={"username": username, "password": password})
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}, auth_callbacks.py", no_update, no_update  # Handle network errors
    
    print("API Response:", response_data)

    if response.status_code == 200 and ctx.triggered_id == "login-btn":
        return "Success! Redirecting...", username, "/dashboard"
        
    if response.status_code == 201 and ctx.triggered_id == "signup-btn":
        return "Account created! You can now log in.", no_update, no_update
    
    return response.json().get("error", "An error occurred"), no_update, no_update

