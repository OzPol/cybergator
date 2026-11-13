from dash import callback, Input, Output
from app.utils.generate_sue_graph import generate_graph_system
from app.services.sue_graph_service import get_sue_data

@callback(
    Output("graph-visualization", "src"),  
    Input("graph-trigger", "data"),  
    Input("url", "pathname")  
)
def fetch_data(trigger, pathname):
    """Fetch stored graph data from Flask API and generate graph image."""
    print(f"🔄 User visited {pathname}. Fetching latest data...")

    if pathname != "/sue-graph":
        return "/assets/system_graph.svg"

    try:
        data = get_sue_data()

        print("✅ Graph data fetched. Generating image...")

        # Generate and save the graph image
        generate_graph_system(data)

        return "/assets/system_graph.svg"
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return ""
