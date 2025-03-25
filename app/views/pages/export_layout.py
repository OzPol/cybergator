from dash import html
import dash_bootstrap_components as dbc

def export_layout():
    return dbc.Container([
        html.H2("Export Data", className="text-center mb-4"),

        # New body copy section
        dbc.Row([
            dbc.Col([
                html.P("CyberGator allows users to generate detailed reports on their system’s resilience assessments.", className="mb-3 text-center"),
                html.Ul([
                    html.Li("Download reports in CSV format."),
                    html.Li("Share findings with security teams for further analysis."),
                    html.Li("Maintain historical records to track improvements over time."),
                ], className="mb-3"),
                html.P("These reports provide valuable documentation for cybersecurity planning and compliance audits.", className="mb-4 text-center"),
            ], width=12)
        ]),

        # Instructional subtitle
        html.P("Select which Data Table and Scores to export.", className="text-center mb-4"),

        # Checklist
        dbc.Checklist(
            options=[
                {"label": "Data Table A", "value": "A"},
                {"label": "Data Table B", "value": "B"},
                {"label": "Data Table C", "value": "C"}
            ],
            id="data-tables-checklist",
            inline=True,
            className="mb-4"
        ),

        # Export button
        dbc.Button("Export Data to CSV", id="export-button", color="primary", className="w-100"),

    ], className="d-flex flex-column align-items-center mt-5")
