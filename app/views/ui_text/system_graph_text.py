from dash import html
import dash_bootstrap_components as dbc

def system_graph_description():
    return html.Div([
        html.H2("System Graph", className="mb-3 text-center"),
        html.P("This graph visualizes the System Under Evaluation (SUE) using node data.", 
               className="mb-3 text-center"),
        html.P("Each node represents a system component like a server, switch, workstation, SAN, router, or firewall. " +
               "Each edge reflects a direct connection between components.", 
               className="mb-3 text-center"),
        dbc.Button("Click to See System Graph Details", id="toggle-system-info", className="btn btn-primary mb-3", style={"display": "block", "margin-left": "0", "text-align": "left"}),

        dbc.Collapse(
            html.Div(
                [
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("What the Graph Displays", className="mt-2 text-center"),
                            html.Ul([
                                html.Li("Nodes: Represent system components such as servers, workstations, switches, SANs, routers, and firewalls."),
                                html.Li("Edges: Represent direct connections based on the 'connected_to' field in the data."),
                                html.Li("Layout: Uses a fixed 'breadthfirst' layout. Interactivity and styling will be added in future updates."),
                            ], className="mb-4", style={"display": "table", "margin": "0 auto", "text-align": "left"}),

                            html.H4("How Resilience Scores Are Calculated", className="mt-4 text-center"),
                            html.P("Each node begins with a base score of 100. Penalties are applied based on a combination of factors derived from both the data and graph structure:",
                                className="text-center mb-3"),

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
                            ], className="mb-4", style={"display": "table", "margin": "0 auto", "text-align": "left"}),

                            html.P(
                                "All these values are combined to generate a final resilience score per node. " +
                                "Lower scores indicate higher vulnerability and higher priority for defensive action.",
                                className="text-center mb-4"
                            ),

                            html.H4("Why This Graph Matters", className="mt-4 text-center"),
                            html.Ul([
                                html.Li("Helps identify high-risk components based on real topology and metadata."),
                                html.Li("Lets users simulate attack paths and system changes in a non-destructive way."),
                                html.Li("Supports decision-making for patching, segmentation, and redundancy improvements."),
                            ], className="mb-4", style={"display": "table", "margin": "0 auto", "text-align": "left"})
                        ]),
                        className="shadow-sm"
                    )
                ],
                className="d-flex justify-content-center",
                style={"max-width": "800px", "margin": "0 auto"}
            ),
            id="collapse-system-info",
            is_open=False
        )
    ], className="text-center")
