from dash import html
import dash_bootstrap_components as dbc

def system_graph_description():
    return dbc.Container([
        html.P(
            "The System Graph in CyberGator provides a visual representation "
            "of the System Under Evaluation (SUE), mapping out its components "
            "and connections to analyze network security, dependencies, and risk factors."
        ),

        html.P(
            "CyberGator uses Neo4j, a graph database, to enhance the efficiency and accuracy "
            "of system analysis by identifying critical nodes, attack paths, and structural vulnerabilities."
        ),

        html.H5("How the System Graph Works"),
        html.Ul([
            html.Li("Nodes represent system components such as servers, workstations, firewalls, and routers."),
            html.Li("Edges represent connections and dependencies between components."),
            html.Li("Neo4j enables analysis of attack paths and vulnerabilities through graph queries."),
        ]),

        html.H5("The Role of Centrality in Risk Assessment"),
        html.P("CyberGator uses graph centrality metrics to identify key components within the system."),
        html.Ul([
            html.Li("Degree centrality highlights highly connected nodes."),
            html.Li("Betweenness centrality identifies nodes that act as bridges or chokepoints."),
            html.Li("Closeness centrality finds nodes that can rapidly interact with others."),
        ]),

        html.H5("How Users Benefit from the System Graph"),
        html.Ul([
            html.Li("Identify critical nodes requiring enhanced security."),
            html.Li("Simulate attack paths and study their potential spread."),
            html.Li("Evaluate configuration changes before implementing them."),
        ]),

        html.P(
            "By integrating Neo4j and centrality analysis, CyberGator allows users to better understand, "
            "visualize, and protect complex systems against modern threats."
        )
    ], className="mb-5")

