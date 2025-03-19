from dash import html
import dash_bootstrap_components as dbc

def export_layout():
    return dbc.Container([  # This keeps everything in a clean container
        html.H3("Export Data", className="text-center mb-4"),  # Title at the top

        html.P("Select which Data Table and Scores to export to CVE format or whatever other format we choose", className="text-center mb-4"),

        dbc.Checklist(
            options=[
                {"label": "Data Table A", "value": "A"},
                {"label": "Data Table B", "value": "B"},
                {"label": "Data Table C", "value": "C"}
            ],
            id="data-tables-checklist",
            inline=True,  # Make the checkboxes align horizontally
            className="mb-4"
        ),

        dbc.Button("Export Data to CSV", id="export-button", color="primary", className="w-100"),  # Button at the bottom
    ], className="d-flex flex-column align-items-center mt-5")
