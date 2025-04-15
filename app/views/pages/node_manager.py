from dash import html, dcc, dash_table, callback, State, Input, Output, no_update, ctx
import dash_bootstrap_components as dbc
from app.services.data_loader import get_critical_functions, load_json
import os
import json

def get_nodes_data():
    """Load the complete nodes data from JSON file"""
    try:
        # Adjust path as needed for your project structure
        json_path = os.path.join('app', 'data', 'json', 'Nodes_Complete.json')
        with open(json_path, 'r') as f:
            # The file appears to contain a list of node objects
            nodes_data = json.load(f)
        return nodes_data
    except Exception as e:
        print(f"Error loading nodes data: {e}")
        return []

def get_function_node_mapping():
    """Create a mapping of functions to their associated nodes"""
    nodes_data = get_nodes_data()
    function_node_mapping = {}
    
    for node in nodes_data:
        node_id = node.get("node_id")
        critical_functions = node.get("critical_functions", [])
        
        for func_id in critical_functions:
            if func_id not in function_node_mapping:
                function_node_mapping[func_id] = []
            function_node_mapping[func_id].append(node_id)
    
    return function_node_mapping

def update_node_associations(function_id, node_ids):
    """Update function associations in the Nodes_Complete.json file"""
    json_path = os.path.join('app', 'data', 'json', 'Nodes_Complete.json')
    
    try:
        # Load existing nodes data
        with open(json_path, 'r') as f:
            nodes_data = json.load(f)
        
        # Update the nodes: remove function from all nodes not in the list
        for node in nodes_data:
            node_id = node.get("node_id")
            current_functions = node.get("critical_functions", [])
            
            if function_id in current_functions and node_id not in node_ids:
                # Remove function from this node
                current_functions.remove(function_id)
                node["critical_functions"] = current_functions
            elif function_id not in current_functions and node_id in node_ids:
                # Add function to this node
                current_functions.append(function_id)
                node["critical_functions"] = current_functions
        
        # Save updated data back to file
        with open(json_path, 'w') as f:
            json.dump(nodes_data, f, indent=4)
        
        print(f"Successfully updated node associations for function {function_id}")
        return True
    except Exception as e:
        print(f"Error updating node associations: {e}")
        return False

def load_critical_functions_with_nodes():
    """Load critical functions with their associated nodes"""
    functions_data = get_critical_functions()
    function_node_mapping = get_function_node_mapping()
    
    if not functions_data:
        print("ERROR: No function data loaded!") 
        return []
    
    # Format the data for the table
    formatted_data = []
    
    for function in functions_data.get("System_Critical_Functions", []):
        function_id = function["Function_Number"]
        # Get associated nodes for this function
        associated_nodes = function_node_mapping.get(function_id, [])
        
        formatted_data.append({
            "Function Number": function_id,
            "Work Area": function["Work_Area"],
            "Criticality": function["Criticality"],
            "Associated Nodes": ", ".join(associated_nodes),
            "Nodes List": associated_nodes  # For internal use, not displayed
        })
    
    print(f"Functions with Nodes Loaded: {len(formatted_data)} entries") 
    return formatted_data

def get_all_available_nodes():
    """Get all available nodes for selection"""
    nodes_data = get_nodes_data()
    return [
        {"label": f"{node['node_name']} ({node['node_id']})", "value": node["node_id"]}
        for node in nodes_data
    ]

def get_functions_for_node(node_id):
    """Get function IDs associated with a specific node"""
    nodes_data = get_nodes_data()
    
    for node in nodes_data:
        if node["node_id"] == node_id:
            return node.get("critical_functions", [])
    
    return []

def get_node_details(node_id):
    """Get details for a specific node"""
    nodes_data = get_nodes_data()
    
    for node in nodes_data:
        if node["node_id"] == node_id:
            return node
    
    return None

@callback(
    Output("function-selection", "options"),
    Input("refresh-data", "n_clicks")
)
def update_function_dropdown(n_clicks):
    """Update function dropdown with current functions"""
    data = load_critical_functions_with_nodes()
    options = [
        {"label": f"{func['Function Number']} - {func['Work Area']}", "value": func["Function Number"]}
        for func in data
    ]
    return options

@callback(
    Output("function-nodes", "value"),
    Input("function-selection", "value"),
    State("refresh-data", "n_clicks")
)
def load_function_nodes(function_number, n_clicks):
    """Load nodes for the selected function"""
    if not function_number:
        return []
    
    function_node_mapping = get_function_node_mapping()
    return function_node_mapping.get(function_number, [])

@callback(
    [
        Output("node-assignment-status", "children"),
        Output("node-assignment-status", "color"),
        Output("node-assignment-status", "is_open")
    ],
    Input("update-nodes-btn", "n_clicks"),
    [
        State("function-selection", "value"),
        State("function-nodes", "value")
    ],
    prevent_initial_call=True
)
def update_function_node_assignments(n_clicks, function_number, selected_nodes):
    if not n_clicks or not function_number:
        return no_update, no_update, no_update
    
    # Update the node associations
    success = update_node_associations(function_number, selected_nodes or [])
    
    # Return feedback message
    if success:
        return f"Node associations updated for function {function_number}", "success", True
    else:
        return f"Error updating node associations for function {function_number}", "danger", True

@callback(
    [
        Output("node-functions-table", "data"),
        Output("node-details", "children")
    ],
    [
        Input("node-selection", "value"),
        Input("refresh-data", "n_clicks")
    ]
)
def update_node_functions_and_details(node_id, n_clicks):
    """Update the table showing functions for a selected node and display node details"""
    if not node_id:
        return [], no_update
    
    # Get functions for this node
    function_ids = get_functions_for_node(node_id)
    
    # Get function details from critical functions data
    functions_data = get_critical_functions()
    all_functions = {}
    
    if functions_data and "System_Critical_Functions" in functions_data:
        for func in functions_data["System_Critical_Functions"]:
            all_functions[func["Function_Number"]] = func
    
    # Format for display
    formatted_data = []
    for func_id in function_ids:
        if func_id in all_functions:
            func = all_functions[func_id]
            formatted_data.append({
                "Function Number": func["Function_Number"],
                "Work Area": func["Work_Area"],
                "Criticality": func["Criticality"]
            })
    
    # Get node details
    node = get_node_details(node_id)
    if node:
        details_content = [
            html.H5("Node Details"),
            html.Div([
                html.Strong("Node ID: "), html.Span(node["node_id"]),
                html.Br(),
                html.Strong("Node Name: "), html.Span(node["node_name"]),
                html.Br(),
                html.Strong("Node Type: "), html.Span(node["node_type"]),
                html.Br(),
                html.Strong("Risk Factor: "), html.Span(node["risk_factor"]),
                html.Br(),
                html.Strong("Critical Data Stored: "), html.Span(str(node["critical_data_stored"])),
                html.Br(),
                html.Strong("Redundancy: "), html.Span(str(node["redundancy"])),
            ])
        ]
    else:
        details_content = []
    
    return formatted_data, details_content

def node_association_manager_layout():
    # Load data
    all_nodes = get_all_available_nodes()

    return dbc.Container([  
        html.H3("Node Association Manager", className="text-center mt-4"),

        # Navigation buttons
        dbc.Row([
            dbc.Col(
                dcc.Link(
                    dbc.Button("Back to Critical Functions", color="primary", className="me-2"),
                    href="/system-tables/critical-functions"  # Make sure this matches your actual route path
                ),
                width="auto"
            ),
            dbc.Col(
                dbc.Button("Refresh Data", id="refresh-data", color="secondary"),
                width="auto",
                className="ms-auto"  # Right align
            )
        ], className="mb-4"),
        
        # Node Association Section
        html.Div([
            # Function to Node Assignment
            dbc.Card([
                dbc.CardHeader("Assign Nodes to Function"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Function:"),
                            dcc.Dropdown(
                                id="function-selection",
                                options=[],  # Populated via callback
                                placeholder="Select a function",
                                className="mb-3"
                            ),
                            html.Label("Assign Nodes:"),
                            dcc.Dropdown(
                                id="function-nodes",
                                options=all_nodes,
                                multi=True,
                                placeholder="Select nodes for this function",
                                className="mb-3"
                            ),
                            dbc.Button("Update Node Assignments", id="update-nodes-btn", color="primary")
                        ], width=12)
                    ]),
                    dbc.Alert(id="node-assignment-status", is_open=False, duration=4000, className="mt-3")
                ])
            ], className="mb-3", style={"position": "relative", "zIndex": "1000"}),
            
            # Node to Functions View
            dbc.Card([
                dbc.CardHeader("View Functions by Node"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Select Node:"),
                            dcc.Dropdown(
                                id="node-selection",
                                options=all_nodes,
                                placeholder="Select a node to view its functions",
                                className="mb-3"
                            ),
                            # Node Details Section
                            html.Div(id="node-details", className="mb-3"),
                            # Functions Table
                            html.Div([
                                html.H5("Functions assigned to this node:"),
                                dash_table.DataTable(
                                    id="node-functions-table",
                                    columns=[
                                        {"name": "Function Number", "id": "Function Number"},
                                        {"name": "Work Area", "id": "Work Area"},
                                        {"name": "Criticality", "id": "Criticality"}
                                    ],
                                    data=[],
                                    style_table={"overflowX": "auto"},
                                    style_cell={"textAlign": "left"},
                                    style_data_conditional=[
                                        {
                                            "if": {"filter_query": '{Criticality} = "High"'},
                                            "backgroundColor": "red",
                                            "color": "white",
                                        },
                                        {
                                            "if": {"filter_query": '{Criticality} = "Medium"'},
                                            "backgroundColor": "orange",
                                            "color": "black",
                                        },
                                        {
                                            "if": {"filter_query": '{Criticality} = "Low"'},
                                            "backgroundColor": "yellow",
                                            "color": "black",
                                        },
                                    ],
                                )
                            ])
                        ], width=12)
                    ])
                ])
            ])
        ], className="border p-3 rounded bg-light")
    ], fluid=True)