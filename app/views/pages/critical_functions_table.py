# First, let's update the main critical functions page to include a button to the node manager

from dash import html, dcc, dash_table, callback, State, Input, Output, no_update
import dash_bootstrap_components as dbc
from app.services.data_loader import get_critical_functions
import os
import json
import re

def update_json_file(table_data):
    """Update the entire Critical_Functions.json file based on table data"""
    # Path to the Critical_Functions.json file
    json_path = os.path.join('app', 'data', 'json', 'Critical_Functions.json')
    
    try:
        # Format data for JSON
        json_data = {
            "System_Critical_Functions": [
                {
                    "Function_Number": func["Function Number"],
                    "Work_Area": func["Work Area"],
                    "Criticality": func["Criticality"],
                    "Criticality_Value": func["Criticality Value"]
                }
                for func in table_data
            ]
        }
        
        # Save to file
        with open(json_path, 'w') as f:
            json.dump(json_data, f, indent=4)
            
        print(f"Successfully updated Critical_Functions.json with {len(table_data)} functions")
        
    except Exception as e:
        print(f"Error updating Critical_Functions.json: {e}")

def save_to_json(function_number, work_area, criticality, criticality_value):
    """Save the new function to the Critical_Functions.json file"""
    from app.services.data_loader import load_json
    
    # Path to the Critical_Functions.json file
    json_path = os.path.join('app', 'data', 'json', 'Critical_Functions.json')
    
    try:
        # Load existing data
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Create new function entry for JSON
        new_function = {
            "Function_Number": function_number,
            "Work_Area": work_area,
            "Criticality": criticality,
            "Criticality_Value": criticality_value
        }
        
        # Add to data
        data["System_Critical_Functions"].append(new_function)
        
        # Save back to file
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Successfully added function {function_number} to Critical_Functions.json")
        
    except Exception as e:
        print(f"Error saving to Critical_Functions.json: {e}")

def remove_from_json(function_number):
    """Remove a function from Critical_Functions.json and from all nodes in Nodes_Complete.json"""
    # File paths
    critical_path = os.path.join('app', 'data', 'json', 'Critical_Functions.json')
    nodes_path = os.path.join('app', 'data', 'json', 'Nodes_Complete.json')

    try:
        # Load and update Critical_Functions.json
        with open(critical_path, 'r') as f:
            critical_data = json.load(f)
        
        critical_data["System_Critical_Functions"] = [
            f for f in critical_data["System_Critical_Functions"]
            if f["Function_Number"] != function_number
        ]

        with open(critical_path, 'w') as f:
            json.dump(critical_data, f, indent=4)
        print(f"✅ Removed function {function_number} from Critical_Functions.json")

        # Load and update Nodes_Complete.json - keep this part as it's handling a different file
        with open(nodes_path, 'r') as f:
            node_data = json.load(f)

        for node in node_data:
            if "critical_functions" in node and function_number in node["critical_functions"]:
                node["critical_functions"] = [
                    fn for fn in node["critical_functions"] if fn != function_number
                ]

        with open(nodes_path, 'w') as f:
            json.dump(node_data, f, indent=4)
        print(f"✅ Removed function {function_number} from all nodes in Nodes_Complete.json")

    except Exception as e:
        print(f"❌ Error removing function: {e}")


def load_critical_functions():
    functions_data = get_critical_functions()

    if not functions_data:
        print("ERROR: No function data loaded!") 
        return []
    
    # Format the data to match the table columns
    formatted_data = [
        {
            "Function Number": function["Function_Number"],
            "Work Area": function["Work_Area"],
            "Criticality": function["Criticality"],
            "Criticality Value": function["Criticality_Value"],
            "Remove": "❎"
        }
        for function in functions_data.get("System_Critical_Functions", [])
    ]
    
    print(f"Critical Functions Loaded: {len(formatted_data)} entries") 
    return formatted_data

def get_next_function_number(current_data):
    """Determine the next function number based on existing functions"""
    if not current_data:
        return "F1"  # Start with F1 if no functions exist
    
    # Extract all function numbers
    function_numbers = [item["Function Number"] for item in current_data]
    
    # Find numeric parts and get the highest number
    max_number = 0
    pattern = re.compile(r'F(\d+)')
    
    for fn in function_numbers:
        match = pattern.match(fn)
        if match:
            num = int(match.group(1))
            max_number = max(max_number, num)
    
    # Return the next function number
    return f"F{max_number + 1}"

def get_criticality_mapping():
    """Get the mapping between criticality levels and their values"""
    functions_data = get_critical_functions()
    
    if not functions_data:
        # Default mapping if no data is available
        return {
            "Low": 1,
            "Medium": 2,
            "High": 3
        }
    
    # Extract unique criticality to value mappings
    criticality_map = {}
    for function in functions_data.get("System_Critical_Functions", []):
        criticality = function.get("Criticality")
        value = function.get("Criticality_Value")
        if criticality and value is not None:
            criticality_map[criticality] = value
    
    # Ensure default values are present
    if "Low" not in criticality_map:
        criticality_map["Low"] = 1
    if "Medium" not in criticality_map:
        criticality_map["Medium"] = 2
    if "High" not in criticality_map:
        criticality_map["High"] = 3
    
    return criticality_map

@callback(
    Output("functions-table", "data", allow_duplicate=True),
    [Input("functions-table", "active_cell")],
    [State("functions-table", "data")],
    prevent_initial_call=True
)
def remove_function(active_cell, data):
    if not active_cell:
        return no_update
    
    row_id = active_cell["row"]
    col_id = active_cell["column_id"]
    
    # Check if Remove column was clicked
    if col_id == "Remove":
        # Get the function number to remove
        function_to_remove = data[row_id]["Function Number"]
        
        # Remove from the table data
        updated_data = data.copy()
        updated_data.pop(row_id)
        
        # Remove from the JSON file
        remove_from_json(function_to_remove)
        
        return updated_data
    
    return no_update

@callback(
    [
        Output("functions-table", "data"),
        Output("new-work-area", "value"),
        Output("new-criticality", "value"),
    ],
    Input("add-function-btn", "n_clicks"),
    [
        State("new-work-area", "value"),
        State("new-criticality", "value"),
        State("functions-table", "data")
    ],
    prevent_initial_call=True
)
def add_new_function(n_clicks, work_area, criticality, current_data):
    # Validate inputs
    if n_clicks is None or not work_area or not criticality:
        return no_update, no_update, no_update
    
    # Get criticality value based on criticality level
    criticality_map = get_criticality_mapping()
    criticality_value = criticality_map.get(criticality, 0)
    
    # Get next function number automatically
    function_number = get_next_function_number(current_data)
    
    # Create new function entry for the table
    new_function = {
        "Function Number": function_number,
        "Work Area": work_area,
        "Criticality": criticality,
        "Criticality Value": criticality_value,
        "Remove": "❎"
    }
    
    # Add to table data
    updated_data = current_data.copy()
    updated_data.append(new_function)
    
    # Update the JSON file
    save_to_json(function_number, work_area, criticality, criticality_value)
    
    # Return updated data and clear input fields
    return updated_data, None, None

@callback(
    Output("functions-table", "data", allow_duplicate=True),
    Input("functions-table", "data_timestamp"),
    State("functions-table", "data"),
    State("functions-table", "data_previous"),
    prevent_initial_call=True
)
def update_functions_data(timestamp, data, previous_data):
    if data == previous_data:
        return no_update
    
    # Check if criticality has changed and update the criticality value
    criticality_map = get_criticality_mapping()
    
    for row in data:
        criticality = row.get("Criticality")
        if criticality in criticality_map:
            row["Criticality Value"] = criticality_map[criticality]
    
    # Update JSON file with all changes
    update_json_file(data)
    
    return data

@callback(
    Output("new-work-area", "options"),
    Input("functions-table", "data")  
)
def populate_work_area_dropdown(_):
    from app.services.data_loader import load_json 
    risk_data = load_json("Risk_Factors.json")
    options = [
        {"label": wa["Work_Area"].replace("_", " "), "value": wa["Work_Area"]}
        for wa in risk_data.get("work_areas", [])
    ]
    return options

def critical_function_layout():
    functions_data = load_critical_functions()
    
    # Get criticality options from existing data
    criticality_map = get_criticality_mapping()
    criticality_options = [
        {"label": f"{level} (Value: {value})", "value": level}
        for level, value in criticality_map.items()
    ]

    return dbc.Container([  
        html.H3("System Critical Functions Table", className="text-center mt-4"),

        # Navigation buttons
        dbc.Row([
            dbc.Col(
                dcc.Link(
                    dbc.Button("Go to System Tables", color="primary", className="me-2"),
                    href="/system-tables"
                ),
                width="auto"
            ),
            dbc.Col(
                dcc.Link(
                    dbc.Button("Manage Node Associations", color="success"),
                    href="/node-association-manager"
                ),
                width="auto"
            ),
            dbc.Col(
                dbc.Button("Reset Functions Table", id="reset-critical-functions", color="warning", className="me-2"),
                width=True,
                className="text-end"
            )
        ], className="mb-3"),

        # Search Bar for Live Filtering
        dcc.Input(id="function-search", type="text", placeholder="Search Functions...", debounce=True),

        dash_table.DataTable(
            id="functions-table",
            columns=[
                {"name": "Function Number", "id": "Function Number"},
                {"name": "Work Area", "id": "Work Area", "editable": True},
                {"name": "Criticality", "id": "Criticality", "editable": True},
                {"name": "Criticality Value", "id": "Criticality Value", "type": "numeric", "editable": False},
                {"name": "Remove", "id": "Remove", "presentation": "markdown"},
            ],
            data=functions_data,  # Load data from JSON
            editable=True,  # Allows inline editing
            filter_action="native",
            sort_action="native",
            row_selectable="multi",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
            style_data_conditional=[
                {
                    "if": {"filter_query": '{Criticality} = "High"'},
                    "backgroundColor": "red",
                    "color": "white",  # Text color white for better contrast
                },
                {
                    "if": {"filter_query": '{Criticality} = "Medium"'},
                    "backgroundColor": "orange",
                    "color": "black",  # Text color black for better contrast
                },
                {
                    "if": {"filter_query": '{Criticality} = "Low"'},
                    "backgroundColor": "yellow",
                    "color": "black",  # Text color black for better contrast
                },
            ],
        ),
        
        # Add New Function Section - Removed function number and criticality value fields
        html.Div([
            html.H4("Add New Function", className="mt-4 mb-3"),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        id="new-work-area", 
                        placeholder="Select Work Area",
                        options=[],  # Populated dynamically
                        clearable=True
                    ),
                    width={"size": 2}
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="new-criticality",
                        placeholder="Select Criticality",
                        options=criticality_options,
                        clearable=True
                    ),
                    width={"size": 2}
                ),
                dbc.Col(
                    dbc.Button("Add Function", id="add-function-btn", color="success", className="w-100"),
                    width={"size": 2}
                ),
            ], className="g-3 mb-4 align-items-end"),
        ], className="border p-3 rounded bg-light")
    ], fluid=True)

@callback(
    Output("functions-table", "data", allow_duplicate=True),
    Input("reset-critical-functions", "n_clicks"),
    prevent_initial_call=True
)
def reset_critical_functions(n_clicks):
    if not n_clicks:
        return no_update

    backup_path = os.path.join('app', 'data', 'backup', 'Critical_Functions.json')
    main_path = os.path.join('app', 'data', 'json', 'Critical_Functions.json')

    try:
        # Load backup and overwrite main file
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)

        with open(main_path, 'w') as f:
            json.dump(backup_data, f, indent=4)

        # Return formatted data to update table
        return [
            {
                "Function Number": f["Function_Number"],
                "Work Area": f["Work_Area"],
                "Criticality": f["Criticality"],
                "Criticality Value": f["Criticality_Value"],
                "Remove": "❎"
            }
            for f in backup_data.get("System_Critical_Functions", [])
        ]
    except Exception as e:
        print(f"Error resetting critical functions: {e}")
        return no_update