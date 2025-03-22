from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from app.services.data_loader import get_critical_functions

def load_critical_functions():
    functions_data = get_critical_functions()

    if not functions_data:
        print("ERROR: No function data loaded!")  # Debugging
        return []
    
    # Format the data to match the table columns
    formatted_data = [
        {
            "Function Number": function["Function_Number"],
            "Work Area": function["Work_Area"],
            "Criticality": function["Criticality"],
            "Criticality Value": function["Criticality_Value"],
            "Remove": "❎"  # Remove button
        }
        for function in functions_data.get("System_Critical_Functions", [])
    ]
    
    print(f"Critical Functions Loaded: {len(formatted_data)} entries")  # Debugging
    return formatted_data

def critical_function_layout():
    functions_data = load_critical_functions()

    return dbc.Container([  
        html.H3("System Critical Functions Table", className="text-center mt-4"),

        html.Div(
            dcc.Link(
                dbc.Button("Go to System Tables", color="primary", className="mb-3"),
                href="/system-tables"
            )
        ),

        # Search Bar for Live Filtering
        dcc.Input(id="function-search", type="text", placeholder="Search Functions...", debounce=True),

        dash_table.DataTable(
            id="functions-table",
            columns=[
                {"name": "Function Number", "id": "Function Number"},
                {"name": "Work Area", "id": "Work Area", "editable": True},
                {"name": "Criticality", "id": "Criticality", "editable": True},
                {"name": "Criticality Value", "id": "Criticality Value", "type": "numeric"},
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
        
        # Add New Function Section
        html.H4("Add New Function"),
        dcc.Input(id="new-function-number", type="text", placeholder="Function Number"),
        dcc.Input(id="new-work-area", type="text", placeholder="Work Area"),
        dcc.Input(id="new-criticality", type="text", placeholder="Criticality"),
        dcc.Input(id="new-criticality-value", type="number", placeholder="Criticality Value"),
        dbc.Button("Add Function", id="add-function-btn", color="success"),
    ], fluid=True)