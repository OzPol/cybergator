from dash import callback, Output, Input, State, dcc, html, no_update
import pandas as pd
from app.views.pages.software_unique_table import load_unique_software
from app.views.pages.cves_table import load_cve_data
from app.views.pages.software_table import load_software_data
from app.views.pages.critical_functions_table import load_critical_functions
from app.services.data_loader import get_nodes

def register_export_callbacks(app):
    """
    Register callbacks related to data export functionality.
    """

    @app.callback(
        [Output("download-nodes", "data"),
         Output("download-cves", "data"),
         Output("download-software-nodes", "data"),
         Output("download-critical-functions", "data"),
         Output("download-software-unique", "data")],
        Input("export-button", "n_clicks"),
        State("data-tables-checklist", "value"),
        prevent_initial_call=True
    )

    def export_selected_data(n_clicks, selected_tables):

        """
        Export data to CSV based on selected tables. Download component with the appropriate CSV data
        """
        if not n_clicks or not selected_tables:
            return None
        
        nodes_data = no_update
        cves_data = no_update
        software_nodes_data = no_update
        critical_functions_data = no_update
        software_unique_data = no_update
        
        # Track which files will be downloaded
        downloaded_tables = []
        
        if "nodes" in selected_tables:
            nodes_list = get_nodes();
        
            df_nodes = pd.DataFrame(nodes_list)

            if "Remove" in df_nodes.columns:
                df_nodes = df_nodes.drop(columns=["Remove"]) 
            nodes_data = dcc.send_data_frame(df_nodes.to_csv, filename="nodes.csv", index=False)

            downloaded_tables.append("Nodes")


        if "cves" in selected_tables:
            cves_list = load_cve_data()
            df_cves = pd.DataFrame(cves_list)

            if "Remove" in df_cves.columns:
                df_cves = df_cves.drop(columns=["Remove"])
            cves_data = dcc.send_data_frame(df_cves.to_csv, filename="cves.csv", index=False)


            downloaded_tables.append("CVEs")
            
        
        if "software-nodes" in selected_tables:
            software_list_all = load_software_data()

            df_software = pd.DataFrame(software_list_all)

            if "Remove" in df_software.columns:
                df_software = df_software.drop(columns=["Remove"])

            software_nodes_data = dcc.send_data_frame(df_software.to_csv, filename="AllSoftware.csv", index=False)

            downloaded_tables.append("Software Nodes")

        
        if "critical-functions" in selected_tables:
            critical_function_list = load_critical_functions()

            df_critical = pd.DataFrame(critical_function_list)

            if "Remove" in df_critical.columns:
                df_critical = df_critical.drop(columns=["Remove"])

            critical_functions_data = dcc.send_data_frame(df_critical.to_csv, filename="CriticalFunctions.csv", index=False)

            downloaded_tables.append("Critical Functions")
            
        
        # Check if unique software is selected
        if "software-unique" in selected_tables:
            # Get the unique software data
            software_list = load_unique_software()
            
            # Convert to DataFrame
            df_unique_software = pd.DataFrame(software_list)
            
            # Remove UI control columns
            if "Expand" in df_unique_software.columns:
                df_unique_software = df_unique_software.drop(columns=["Expand"])
            if "Remove" in df_unique_software.columns:
                df_unique_software = df_unique_software.drop(columns=["Remove"])
            
            software_unique_data = dcc.send_data_frame(df_unique_software.to_csv, filename="uniqueSoftware.csv", index=False)
            # Return as a downloadable CSV
            # return dcc.send_data_frame(df_unique_software.to_csv, filename="uniqueSoftware.csv")
        
        
        
        return nodes_data, cves_data, software_nodes_data, critical_functions_data, software_unique_data