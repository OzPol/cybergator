from dash import html, dash_table
import dash_bootstrap_components as dbc
import json
import os
import pandas as pd

def system_tables():
    # Construct the path to the JSON file
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Go up to the 'app' directory
    Attack_Tree_json_path = os.path.join(base_dir, 'data', 'json', 'Attack_Tree.json')
    Critical_Function_json_path = os.path.join(base_dir, 'data', 'json', 'Critical_Functions.json')
    Fuzzy_Set_json_path = os.path.join(base_dir, 'data', 'json', 'Fuzzy_Set.json')
    Nodes_Complete_json_path = os.path.join(base_dir, 'data', 'json', 'Nodes_Complete.json')
    Risk_Factors_json_path = os.path.join(base_dir, 'data', 'json', 'Risk_Factors.json')

    # Load the JSON data
    with open(Attack_Tree_json_path, 'r') as file:
        attack_tree_data = json.load(file)
    with open(Critical_Function_json_path, 'r') as file:
        critical_function_data = json.load(file)
    # with open(Fuzzy_Set_json_path, 'r') as file:
    #     attack_tree_data = json.load(file)    
    # with open(Nodes_Complete_json_path, 'r') as file:
    #     attack_tree_data = json.load(file)
    with open(Risk_Factors_json_path, 'r') as file:
        risk_factors_data = json.load(file)

    # Extract the attack goals and steps
    attack_goals = attack_tree_data['attack_goals']
    critical_functions = critical_function_data.get("System_Critical_Functions", [])
    work_areas = risk_factors_data.get("work_areas", [])

    # Create a list to hold the rows of the table
    attack_tree_rows = []
    critical_functions_rows = []
    risk_factors_rows = []
    
    # Iterate through each goal and step to populate the rows
    for goal in attack_goals:
        for step in goal['steps']:
            row = {
                'Goal ID': goal['goal_id'],
                'Goal Name': goal['goal_name'],
                'Step ID': step['step_id'],
                'Step Name': step['name'],
                'CVE': step['cve'],
                'Tactic': step['tactic'],
                'Technique': step['technique'],
                'Subtechnique': step.get('subtechnique', 'N/A'),  # Use .get() with a default value
                'Critical Functions Impacted': ', '.join(step['critical_functions_impacted']),
                'Probability': step['probability'],
                'Next State': step['next_state']
            }
            attack_tree_rows.append(row)
    
    for function in critical_functions:
        row = {
            'Function Number': function.get('Function_Number', 'N/A'),  # Use .get() with a default value
            'Work Area': function.get('Work_Area', 'N/A'),
            'Criticality': function.get('Criticality', 'N/A'),
            'Criticality Value': function.get('Criticality_Value', 'N/A')
        }
        critical_functions_rows.append(row)

    for work_area in work_areas:
        work_area_name = work_area.get("work_areas", "N/A")
        risk_factors = work_area.get("Risk_Factors_Matrix", {})
        row = {"Work Area": work_area_name}
        row.update(risk_factors)  # Add all risk factors to the row
        risk_factors_rows.append(row)

    # Convert the list of rows into a DataFrame
    attack_tree_df = pd.DataFrame(attack_tree_rows)
    critical_function_df = pd.DataFrame(critical_functions_rows)
    risk_factors_df = pd.DataFrame(risk_factors_rows)
    
    # Create the Dash table component for Attack Tree
    attack_tree_table = dash_table.DataTable(
        id='attack-tree-table',
        columns=[{"name": i, "id": i} for i in attack_tree_df.columns],
        data=attack_tree_df.to_dict('records'),
        style_table={'overflowX': 'auto'},  # Allow horizontal scrolling if needed
        style_cell={
            'textAlign': 'left',
            'padding': '5px',  # Reduce cell padding
            'fontSize': '12px',  # Reduce font size
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'fontSize': '12px',  # Reduce header font size
            'padding': '5px',  # Reduce header padding
        },
        style_data={
            'fontSize': '12px',  # Reduce data font size
            'padding': '5px',  # Reduce data cell padding
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )

    critical_functions_table = dash_table.DataTable(
        id='critical-functions-table',
        columns=[{"name": i, "id": i} for i in critical_function_df.columns],
        data=critical_function_df.to_dict('records'),
        style_table={'overflowX': 'auto'},  # Allow horizontal scrolling if needed
        style_cell={
            'textAlign': 'left',
            'padding': '5px',  # Reduce cell padding
            'fontSize': '12px',  # Reduce font size
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'fontSize': '12px',  # Reduce header font size
            'padding': '5px',  # Reduce header padding
        },
        style_data={
            'fontSize': '12px',  # Reduce data font size
            'padding': '5px',  # Reduce data cell padding
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )

    risk_factors_table = dash_table.DataTable(
        id='risk-factors-table',
        columns=[{"name": i, "id": i} for i in risk_factors_df.columns],
        data=risk_factors_df.to_dict('records'),
        style_table={'overflowX': 'auto'},  # Allow horizontal scrolling if needed
        style_cell={
            'textAlign': 'left',
            'padding': '5px',  # Reduce cell padding
            'fontSize': '12px',  # Reduce font size
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'fontSize': '12px',  # Reduce header font size
            'padding': '5px',  # Reduce header padding
        },
        style_data={
            'fontSize': '12px',  # Reduce data font size
            'padding': '5px',  # Reduce data cell padding
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )

    # Create the accordion layout
    accordion = dbc.Accordion(
        [
            dbc.AccordionItem(
                children=[attack_tree_table],  # Attack Tree table
                title="Attack Tree",  # Title of the tab
                item_id="attack-tree"  # Unique ID for this tab
            ),
            dbc.AccordionItem(
                children=[critical_functions_table],  # Placeholder for Critical Functions
                title="Critical Functions",  # Title of the tab
                item_id="critical-functions"  # Unique ID for this tab
            ),
            dbc.AccordionItem(
                children=[html.Div("Fuzzy Set table will go here.")],  # Placeholder for Fuzzy Set
                title="Fuzzy Set",  # Title of the tab
                item_id="fuzzy-set"  # Unique ID for this tab
            ),
            dbc.AccordionItem(
                children=[html.Div("Nodes Complete table will go here.")],  # Placeholder for Nodes Complete
                title="Nodes Complete",  # Title of the tab
                item_id="nodes-complete"  # Unique ID for this tab
            ),
            dbc.AccordionItem(
                children=[risk_factors_table],  # Placeholder for Risk Factor
                title="Risk Factor",  # Title of the tab
                item_id="risk-factor"  # Unique ID for this tab
            ),
        ],
        id="accordion",  # ID for the accordion component
        active_item="",  # Default open tab
        flush=True,  # Remove borders for a cleaner look
    )

    # Return the accordion layout
    return accordion

