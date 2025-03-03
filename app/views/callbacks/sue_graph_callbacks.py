from dash import callback, Input, Output
import requests
from app.utils.generate_sue_graph import generate_graph_system

API_BASE_URL = "http://localhost:8000/api/sue-graph"

@callback(
    Output("graph-visualization", "src"),  
    Input("graph-trigger", "data"),  
    Input("url", "pathname")  
)
def fetch_data(trigger, pathname):
    """Fetch stored graph data from Flask API and generate graph image."""
    print(f"🔄 User visited {pathname}. Fetching latest data...")

    if pathname != "/sue-graph":
        return "/assets/system_graph.png"  

    try:
        response = requests.get(f"{API_BASE_URL}/")
        response.raise_for_status()
        data = response.json()

        print("✅ Graph data fetched. Generating image...")

        # Generate and save the graph image
        generate_graph_system(data)

        return "/assets/system_graph.png"  # Dash auto-updates image
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return "/assets/error.png"  # Fallback fake image
