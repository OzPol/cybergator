from dash import html
import dash_bootstrap_components as dbc

def system_graph_description():
    return html.Div([
        
        html.H5("System Graph Overview", className="btn btn-primary mb-3"),
        html.H5("   This graph visualizes the System Under Evaluation (SUE) using nodes' data.", className="mt-3"),
        html.H5("   Each node represents a system component like a server, switch, workstation, SAN, router, or firewall.", className="mt-3"),
        html.H5("   Each edge reflects a direct connection between components.", className="mt-3"),
        html.H5("   ", className="mt-3"),
        dbc.Button("Click to See System Graph Details", id="toggle-system-info", className="btn btn-primary mb-3"),

        dbc.Collapse(
            dbc.Container([

                html.H5("What the Graph Displays", className="mt-3"),
                html.Ul([
                    html.Li("Nodes: Represent system components such as servers, workstations, switches, SANs, routers, and firewalls."),
                    html.Li("Edges: Represent direct connections based on the 'connected_to' field in the data."),
                    html.Li("Layout: Uses a fixed 'breadthfirst' layout. Interactivity and styling will be added in future updates."),
                ], className="mb-4"),

                html.H5("How Resilience Scores Are Calculated", className="mt-3"),
                html.P("Each node begins with a base score of 100. Penalties are applied based on a combination of factors derived from both the data and graph structure:"),

                html.Ul([
                    html.Li("CVE Vulnerabilities: Penalty is based on the summed NVD CVE scores associated with each node's installed software."),
                    html.Li("Centrality Score: Average of four graph metrics computed using NetworkX:"),
                    html.Ul([
                        html.Li("Degree Centrality: Higher if the node has many direct connections."),
                        html.Li("Betweenness Centrality: Higher if the node lies on many shortest paths between others."),
                        html.Li("Closeness Centrality: Higher if the node can reach all others with fewer hops."),
                        html.Li("Eigenvector Centrality: Higher if connected to other well-connected nodes."),
                    ]),
                    html.Li("Connectedness: Nodes with more direct connections are penalized to reflect greater potential blast radius."),
                    html.Li("Switch Dependency: Fixed penalty for relying on switches or other intermediaries."),
                    html.Li("Redundancy: Nodes marked as redundant receive a small bonus."),
                    html.Li("Criticality: Penalty increases based on the weights of assigned critical functions."),
                    html.Li("Environmental Risk: Computed using fuzzy logic from external factors, then applied as a divisor on the score."),
                ]),

                html.P(
                    "All these values are combined to generate a final resilience score per node. "
                    "Lower scores indicate higher vulnerability and higher priority for defensive action."
                ),

                html.H5("Why This Graph Matters", className="mt-4"),
                html.Ul([
                    html.Li("Helps identify high-risk components based on real topology and metadata."),
                    html.Li("Lets users simulate attack paths and system changes in a non-destructive way."),
                    html.Li("Supports decision-making for patching, segmentation, and redundancy improvements."),
                ])
            ]),
            id="collapse-system-info",
            is_open=False
        )
    ])
