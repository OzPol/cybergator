from dash import html
import dash_bootstrap_components as dbc

def homepage_layout():
    return html.Div([  
        dbc.Container([  # Wrapped everything in a centered container
            # Introduction Section
            dbc.Row([  
                dbc.Col([  
                    html.H2("Introduction to CyberGator", className="section-title mb-2 text-center"),
                    html.P("CyberGator is a cyber resilience assessment tool designed to help organizations evaluate and improve "
                    "their system security. Using a combination of attack path analysis, Bayesian modeling, and fuzzy logic-based "
                    "risk scoring, CyberGator provides a structured way to measure vulnerabilities and simulate potential threats.",
                           className="mb-3 text-center"),

                    html.P("Organizations face an ever-evolving cyber threat landscape, and traditional risk assessments often "
                    "fall short in adapting to new attack strategies. CyberGator bridges this gap by offering real-time insights"
                    " into how systems respond to different threats, allowing users to make informed security decisions.",
                           className="mb-3 text-center"),

                    html.P("By uploading a System Under Evaluation (SUE), users can interact with their system data, simulate "
                    "attacks, test environmental risk factors, and analyze resilience without making irreversible changes to "
                    "their infrastructure. This makes CyberGator an essential tool for cybersecurity professionals looking to "
                    "strengthen their organization's defenses.",
                           className="mb-3 text-center"),
                ], width=12)
            ], className="mt-4 mb-2"),  

            # Meet Our Team Section
            dbc.Row([  
                dbc.Col([  
                    html.H2("Meet Our Team", className="section-title mb-4 text-center"),

                    # First Row: 3 Team Cards
                    dbc.Row([  
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Ozlem_Polat.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Ozlem Polat - Project Lead and SCRUM Master", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Samson_Carter.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Samson carter - Project Manager", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Jess_Lourenco.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Jess Lourenco - Backend Lead", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),
                    ], className="justify-content-center"),  # Centers the cards in the row

                    # Second Row: 2 Team Cards
                    dbc.Row([  
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Andrew_Ballard.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Andrew Ballard - Frontend Team", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Shayan_Akhoondan.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Shayan Akhoondan - Frontend Team", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),
                    ], className="justify-content-center"),  
                ], width=12)
            ], className="mb-5"),  

             # How to Use the App Section (Simulation Mode Explanation)
            dbc.Row([
                dbc.Col([
                    html.H2("How to Use the App", className="section-title mb-2 text-center"),
                    html.P("Once users become familiar with CyberGator by exploring the preloaded System Under Evaluation, "
                    "they can begin experimenting with the application's features in a controlled environment. The preloaded SUE "
                    "provides a realistic simulation of a network with existing system components, allowing users to test various "
                    "configurations, run simulations, and observe the impact of their changes without affecting any live data. This "
                    "hands-on practice helps users understand how CyberGator functions and how different parameters influence their "
                    "system’s resilience score.", className="section-subtitle mb-3 text-center"),

                    html.P("Once comfortable with the basics, users can start uploading their own system data, including "
                    "workstations, servers, and network components. This allows for a more personalized experience as they begin "
                    "tailoring CyberGator to evaluate their unique system configurations. Whether testing environmental factors "
                    "or running advanced attack simulations, users can interact with their custom SUE to assess vulnerabilities "
                    "and improve overall system security. The ability to upload and manipulate their own nodes enables users to "
                    "apply their newfound knowledge to real-world scenarios and continue strengthening their organization’s "
                    "cybersecurity posture.", className="section-subtitle mb-3 text-center"),
                    html.Div([
                        html.H3("What is Simulation Mode?", className="text-center"),
                        html.P("Simulation Mode allows users to safely test modifications to their system without affecting the "
                        "actual database. When enabled, any changes made to system components, environmental factors, or security"
                        " settings will only apply within the simulation environment. This allows users to experiment with "
                        "different configurations, test responses to threats, and observe how their Resilience Score is "
                        "impacted—without permanently altering the database.",
                               className="mb-4 text-center"),
                        html.P("Users can:", className="mb-1 text-center"),
                        html.Ul([
                            html.Li("Adjust system parameters and attack scenarios to observe outcomes."),
                            html.Li("Analyze how different security measures affect resilience."),
                            html.Li("Export simulation results for documentation and decision-making."),
                        ], className="text-center mb-4"),
                        html.P("Once Simulation Mode is toggled off, all temporary modifications are discarded, ensuring the "
                        "integrity of the actual system remains intact.",
                               className="text-center mb-3"),
                        html.P("Navigation is done via the menu on the left, where users can access different sections to "
                        "view and edit the uploaded SUE.", className="text-center"),
                    ], className="p-4 border rounded bg-light text-center")
                ], width=12)
            ], className="mb-5"),

        ], className="d-flex flex-column align-items-center",  # Centers content in the page
        style={"maxWidth": "80%", "margin": "0 auto"})  # Adjusts width and centers
    ])