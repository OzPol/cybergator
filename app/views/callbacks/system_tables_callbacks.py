from dash import Input, Output, State, html
import dash

def register_system_tables_callbacks(app):
    """Register callbacks to handle system table selection."""

    @app.callback(
        Output("selected-table", "data"),  # Stores which table is selected
        [Input("nodes-table-btn", "n_clicks"),
        Input("cves-table-btn", "n_clicks")],
        prevent_initial_call=True
    )
    def select_table(nodes_clicks, cves_clicks):
        """Updates selected table based on button clicked."""
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        return triggered_id  # Stores selected table

    @app.callback(
        Output("table-content", "children"),
        Input("selected-table", "data")
    )
    def update_table_content(selected_table):
        """Loads table content dynamically."""
        if selected_table == "nodes-table-btn":
            return html.Div([
                html.H4("Nodes Table"),
                html.P("This will show the full nodes table.")
            ])
        elif selected_table == "cves-table-btn":
            return html.Div([
                html.H4("CVEs Table"),
                html.P("This will show the full CVEs table.")
            ])
        return html.Div("Select a table to view its contents.")
