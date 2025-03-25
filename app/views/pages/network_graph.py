from dash import html, dcc
import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

def cytoscape_graph(graph_data):
    # Creates Cytoscape graph elements from JSON data
    elements = [
        {"data": {"id": node["data"]["id"], "label": node["data"]["label"]}} for node in graph_data["nodes"]
    ] + [
        {"data": {"source": edge["data"]["source"], "target": edge["data"]["target"]}} for edge in graph_data["edges"]
    ]
    return elements


def graph_layout():
    # Graph Layout Page
    return html.Div([
        html.H3("System Graph", className="text-center mb-4"),

        # Descriptive body copy
        dbc.Container([
            html.P("The System Graph in CyberGator provides a visual representation of the System Under Evaluation (SUE), mapping out its "
            "components and connections to analyze network security, dependencies, and risk factors.", className="mb-3"),
            html.P("CyberGator uses Neo4j, a graph database, to enhance the efficiency and accuracy of system analysis by identifying critical "
            "nodes, attack paths, and structural vulnerabilities.", className="mb-3"),

            html.H5("How the System Graph Works", className="mt-4"),
            html.Ul([
                html.Li("Nodes Represent System Components – Each node corresponds to a server, workstation, firewall, router, or database, "
                "with attributes such as function, vulnerabilities (CVE data), and risk levels."),
                html.Li("Edges Define Relationships – Edges represent connections and dependencies between components, helping visualize "
                "how an attack could spread."),
                html.Li("Neo4j Graph Analysis – Users can run queries to trace attack paths, identify weak points, and simulate system changes"
                " without affecting the live database."),
            ], className="mb-3"),

            html.H5("The Role of Centrality in Risk Assessment", className="mt-4"),
            html.P("CyberGator uses graph centrality algorithms to highlight key system components that are most influential in network security.", className="mb-2"),
            html.Ul([
                html.Li("Degree Centrality – Nodes with many connections (e.g., central servers) are high-risk targets for attackers."),
                html.Li("Betweenness Centrality – Nodes that act as bridges can allow lateral movement in an attack if compromised."),
                html.Li("Closeness Centrality – Components that can quickly communicate with others may be critical points for security monitoring."),
            ], className="mb-3"),

            html.H5("How Users Benefit from the System Graph", className="mt-4"),
            html.Ul([
                html.Li("Identify Critical Nodes – Pinpoint system components that require stronger protections based on their centrality."),
                html.Li("Analyze Attack Paths – Simulate how threats move through the network to improve defensive strategies."),
                html.Li("Test System Changes – Modify system configurations in Simulation Mode to see how updates impact resilience before "
                "applying them permanently."),
            ], className="mb-3"),

            html.P("By integrating Neo4j and centrality metrics, CyberGator ensures that security teams can better understand, visualize, "
            "and defend their systems from evolving threats.", className="mb-5"),
        ]),

        html.H5("Interactive System Graph", className="text-center mt-4 mb-2"),

        html.Button("Refresh Graph", id="refresh-graph-btn", n_clicks=1, className="btn btn-primary mb-3 d-block mx-auto"),

        # Graph with styled border
        html.Div(
            children=[
                cyto.Cytoscape(
                    id="system-graph",
                    layout={"name": "breadthfirst"},
                    style={"width": "100%", "height": "800px"},
                    elements=[],
                )
            ],
            style={
                "border": "3px solid #007BFF",
                "borderRadius": "10px",
                "padding": "10px",
                "marginTop": "10px",
                "marginBottom": "40px",
                "backgroundColor": "#f9f9f9"
            }
        ),
    ])
