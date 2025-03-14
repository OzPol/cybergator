from dash import Input, Output, callback
import requests

def register_resilience_callbacks(app):
    """ Registers callbacks to update the resilience score dynamically. """
    
    @app.callback(
        Output("system-resilience-score", "children"),
        Input("session-user", "data"),
    )
    def update_resilience_score(session_user):
        """Fetch system resilience score when user is logged in."""
        if not session_user:
            return ""  # Don't display anything if user is not logged in
        
        response = requests.get("http://127.0.0.1:8000/api/resilience")
        
        if response.status_code == 200:
            data = response.json()
            score = round(data["system_resilience_score"], 4)
            return f"System Resilience Score: {score}"
        
        return "Error fetching resilience score"
