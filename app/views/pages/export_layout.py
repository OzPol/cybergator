from dash import html
import dash_bootstrap_components as dbc

# Table list that matches table pages in app/views/pages
system_tables_options = [
    {"label": "Nodes", "value": "nodes"},
    {"label": "CVEs", "value": "cves"},
    {"label": "Software Nodes", "value": "software-nodes"},
    {"label": "Critical Functions", "value": "critical-functions"},
    {"label": "Unique Software", "value": "software-unique"},
]

def export_layout():
    return dbc.Container([
        html.H2("Export Data", className="text-center mb-4"),

        # New body copy section
        dbc.Row([
            dbc.Col([
                html.P("CyberGator allows users to generate detailed reports on their system’s resilience assessments.", className="mb-3 text-center"),
                html.Div([
                    html.Ul([
                        html.Li("Download reports in CSV or PDF format."),
                        html.Li("Share findings with security teams for further analysis."),
                        html.Li("Maintain historical records to track improvements over time."),
                    ])
                ], className="mb-3", style={"maxWidth": "800px", "margin": "0 auto"}),  # centers and limits width

                html.P("These reports provide valuable documentation for cybersecurity planning and compliance audits.", className="mb-4 text-center"),
            ], width=12)
        ]),

        # Instructional subtitle
        html.P("Select which Data Table and Scores to export.", className="text-center mb-4"),

        # Checklist
        dbc.Checklist(
            options=system_tables_options,
            id="data-tables-checklist",
            inline=True,
            className="mb-4"
        ),

        # Export button
        dbc.Button("Export Data to CSV", id="export-button", color="primary", className="w-100"),

    ], className="d-flex flex-column align-items-center mt-5")
