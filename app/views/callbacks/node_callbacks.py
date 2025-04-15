from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from app.services.node_service import add_node_to_system_graph
from app.services.data_loader import get_software_metadata

def register_node_callbacks(app):
    @app.callback(
        Output("node-feedback", "children"),
        Input("submit-new-node", "n_clicks"),
        State("node-id-input", "value"),
        State("node-name-input", "value"),
        State("node-type-selector", "value"),
        State("rack-selector", "value"),
        State("category-selector", "value"),
        State("critical-function-selector", "value"),
        State("connected-nodes-selector", "value"),
        State("backup-role", "value"),
        State("data-redundancy-selector", "value"),
        State("risk-factor-selector", "value"),
        State("switch-dependency-check", "value"),
        State("software-make-selector", "value"),
        State("software-version-selector", "value"),
    )
    def handle_create_node(n_clicks, node_id, node_name, node_type, rack_name, category,
                        critical_functions, connected_to, backup_role,
                        data_redundancy, risk_factor, switch_dependency_list,
                        software_make, software_version):

        from dash.exceptions import PreventUpdate
        from app.services.node_service import add_node_to_system_graph
        from app.services.data_loader import get_software_metadata

        if n_clicks == 0 or not node_id or not node_name:
            raise PreventUpdate

        try:
            switch_dependency = True if switch_dependency_list and "yes" in switch_dependency_list else False

            software_meta = get_software_metadata(software_make, software_version)
            resilience_penalty = 0.0
            if connected_to is None:
                connected_to = []

            add_node_to_system_graph(
                node_id=node_id,
                node_name=node_name,
                node_type=node_type,
                critical_functions=critical_functions or [],
                connected_to=connected_to,
                backup_role=backup_role,
                data_redundancy=data_redundancy,
                risk_factor=risk_factor,
                switch_dependency=switch_dependency,
                resilience_penalty=resilience_penalty,
                software_make=software_make,
                software_version=software_version,
                rack_name=rack_name,
                category=category
            )

            return f"Node '{node_id}' added successfully."

        except Exception as e:
            return f"Error: {str(e)}"
        