from dash import callback, Output, Input, State, dcc, html
import pandas as pd
from app.views.pages.software_unique_table import load_unique_software

def register_export_callbacks(app):
    """
    Register callbacks related to data export functionality.
    """

    @app.callback(
        Output("download-data", "data"),
        Input("export-button", "n_clicks"),
        State("data-tables-checklist", "value"),
        prevent_initial_call=True
    )

    def export_selected_data(n_clicks, selected_tables):

        """
        Export data to CSV based on selected tables.
        
        Args:
            n_clicks: Number of times the export button has been clicked
            selected_tables: List of table types selected for export
            
        Returns:
            Download component with the appropriate CSV data
        """
        if not n_clicks or not selected_tables:
            return None
        
        # Check if unique software is selected
        if "software-unique" in selected_tables:
            # Get the unique software data
            software_list = load_unique_software()
            
            # Convert to DataFrame
            df = pd.DataFrame(software_list)
            
            # Remove UI control columns
            if "Expand" in df.columns:
                df = df.drop(columns=["Expand"])
            if "Remove" in df.columns:
                df = df.drop(columns=["Remove"])
            
            # Return as a downloadable CSV
            return dcc.send_data_frame(df.to_csv, filename="uniqueSoftware.csv", index=False)
        
        
        
        return None