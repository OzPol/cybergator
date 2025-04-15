from dash import Input, Output, State, no_update
import requests

def register_resilience_callbacks(app):

    # First callback to load the resilience score on user login or refresh
    @app.callback(
        Output("system-resilience-score", "children"),
        Input("session-user", "data"),
        prevent_initial_call=False
    )
    def load_initial_resilience(session_user):
        """Fetch system resilience score on initial load and session changes"""
        if not session_user:
            return ""
        
        try:
            response = requests.get("http://localhost:8000/api/resilience")
            if response.status_code == 200:
                data = response.json()
                score = round(data["system_resilience_score"], 4)
                return f"System Resilience Score: {score}"
            return "N/A"
        except Exception as e:
            return f"Error: {str(e)}"

    # Second callback to trigger a manual resilience calculation when button is clicked
    @app.callback(
        [Output("resilience-recalculate-feedback", "children"),
         Output("resilience-update-trigger", "children")],
        Input("recalculate-resilience-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def manual_recalculate(n_clicks):
        try:
            response = requests.get("http://127.0.0.1:8000/api/resilience")
            if response.status_code == 200:
                # Show message and update trigger
                return "✅ Recalculating...", str(n_clicks)
            return "❌ Failed to recalculate.", no_update
        except Exception as e:
            return f"⚠️ Error: {str(e)}", no_update
    
    # Third callback to update displayed resilience score when recalculation is triggered
    @app.callback(
        [Output("system-resilience-score", "children", allow_duplicate=True),
         Output("resilience-recalculate-feedback", "children", allow_duplicate=True)],
        Input("resilience-update-trigger", "children"),
        State("system-resilience-score", "children"),
        prevent_initial_call=True  # This must be True when using allow_duplicate
    )
    def update_resilience_on_recalculate(update_trigger, _):
        """Update resilience score when manually triggered"""
        if not update_trigger:
            return no_update, no_update
            
        try:      
            response = requests.get("http://localhost:8000/api/resilience")
            if response.status_code == 200:
                data = response.json()
                new_score = round(data["system_resilience_score"], 4)
                score_text = f"System Resilience Score: {new_score}"

                return score_text, "✅ Resilience updated."
        except Exception as e:
            return f"Error: {str(e)}", no_update