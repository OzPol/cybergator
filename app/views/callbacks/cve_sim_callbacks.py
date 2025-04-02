from dash import Input, Output
from app.services.data_loader import get_simulation_nodes

def register_cve_simulation_callbacks(app):
    @app.callback(
        Output("cves-table", "data"),
        Input("refresh-table-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def refresh_cve_table(n_clicks):
        nodes = get_simulation_nodes()
        refreshed_data = []

        for node in nodes:
            for cve_id, nvd_score in node.get("CVE_NVD", {}).items():
                refreshed_data.append({
                    "CVE ID": cve_id,
                    "NVD Score": nvd_score,
                    "Node ID": node["node_id"],
                    "Node Name": node["node_name"],
                    "Remove": "❌"
                })
        return refreshed_data
