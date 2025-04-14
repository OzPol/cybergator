from dash import Input, Output
import requests

def register_resilience_callbacks(app):
    # Registers callbacks to update the resilience score dynamically.

    @app.callback(
        [Output("resilience-recalculate-feedback", "children"),
         Output("resilience-update-trigger", "children")],  # Added trigger output
        Input("recalculate-resilience-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def manual_recalculate(n_clicks):
        try:
            response = requests.get("http://127.0.0.1:8000/api/resilience")
            if response.status_code == 200:
                # Return both the feedback message and a trigger for the score update
                return "✅ Resilience recalculated.", str(n_clicks)
            return "❌ Failed to recalculate.", ""
        except Exception as e:
            return f"⚠️ Error: {str(e)}", ""
    
    @app.callback(
        Output("system-resilience-score", "children"),
        [Input("session-user", "data"),
         Input("resilience-update-trigger", "children")]  # Added this input to listen for updates
    )
    def update_resilience_score(session_user, update_trigger):
        """Fetch system resilience score when user is logged in or when triggered."""
        if not session_user:
            return ""  # Don't display anything if user is not logged in

        try:
            response = requests.get("http://localhost:8000/api/resilience")
            if response.status_code == 200:
                data = response.json()
                score = round(data["system_resilience_score"], 4)
                return f"System Resilience Score: {score}"
        except Exception as e:
            return f"Error: {str(e)}"
        
        return "Error fetching resilience score"
    
    