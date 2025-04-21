from dash import html
import dash_bootstrap_components as dbc

def homepage_layout():
    return html.Div([  
        dbc.Container([  # Wrapped everything in a centered container
            # Introduction Section
            dbc.Card([
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col([
                            html.H2("Introduction to CyberGator", className="fw-bold mb-3"),
                            html.H5("CyberGator is a cyber resilience platform that helps organizations assess, understand & strengthen their systems against modern threats.", className="mb-3"),
                            html.H5("By combining attack path analysis, Bayesian inference, & fuzzy logic-based risk scoring, CyberGator simulates how threats propagate across complex environments.", className="mb-3")
                        ], md=6, className="d-flex flex-column justify-content-center"),
                        dbc.Col([
                            html.Img(src="/assets/icon_intro_illustration.png", style={"width": "100%", "height": "auto", "borderRadius": "6px"})
                        ], md=6),
                    ])
                )
            ], className="mb-4 shadow-sm", style={"width": "100%"}),
            
            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Img(src="assets/icon_risk.png", height="200px", className="mb-2 d-block mx-auto"),
                            html.P("Traditional risk assessments often fall short when adapting to new attack strategies.", className="text-center mb-0")
                        ])
                    ), md=4, className="mb-3"
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Img(src="assets/icon_insights.png", height="200px", className="mb-2 d-block mx-auto"),
                            html.P("CyberGator bridges that gap by providing insights into threat propagation and system response.", className="text-center mb-0")
                        ])
                    ), md=4, className="mb-3"
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Img(src="assets/icon_upload.png", height="200px", className="mb-2 d-block mx-auto"),
                            html.P("Users can upload a System Under Evaluation (SUE) and safely simulate attacks and defensive actions.", className="text-center mb-0")
                        ])
                    ), md=4, className="mb-3"
                )
            ], className="mb-5"),

            dbc.Card([
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col([
                            html.Img(src="/assets/icon_true_risk.png", style={"width": "100%", "height": "auto", "borderRadius": "6px"})
                        ], md=6),
                        dbc.Col([
                            html.H2("Report True Risk of Vulnerabilities", className="fw-bold mb-3"),
                            html.H5("Visualize CVEs by device, software, or asset using holistic, impact-aware dashboards.", className="mb-3"),
                            html.H5("Pivot from intrusion risk to business risk using exploitability data to prioritize real threats.", className="mb-3"),
                            html.H5("Validate & track which vulnerabilities put critical assets in danger & confirm when mitigation works.", className="mb-3")
                        ], md=6, className="d-flex flex-column justify-content-center"),
                    ])
                )
            ], className="mb-4 shadow-sm", style={"width": "100%"}),

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
                                    html.H4("Ozlem Polat", className="card-title"),
                                    html.H6("Team Lead & Scrum Master", className="card-title"),
                                    html.P(
                                    "Data scientist | ML Engineer with a background in manufacturing & product development. Specializes in intelligent systems, formal methods, and complex problem-solving.",
                                    className="card-text"
                                ),
                                    dbc.Button("Read Full Bio", href="/about/oz", color="primary", className="mt-2")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Samson_Carter.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Samson Carter", className="card-title"),
                                    html.H6("Project Manager", className="card-title"),
                                    html.P("Ex-chef turned software developer. Passionate about inclusive leadership, systems thinking, and mission-driven tech.", className="card-text"),
                                    dbc.Button("Read Full Bio", href="/about/samson", color="primary", className="mt-2")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Jess_Lourenco.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Jess Lourenco", className="card-title"),
                                    html.H6("Backend Lead", className="card-title"),
                                    html.P("Ex-product manager turned software engineer. Passionate about backend, open source, and building solutions that improve people's lives.", 
                                        className="card-text"),
                                    dbc.Button("Read Full Bio", href="/about/jess", color="primary", className="mt-2") 
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
                                    html.H4("Andrew Ballard", className="card-title"),
                                    html.H6("Frontend Lead", className="card-title"),
                                    html.P(
                                    "UI/UX-focused developer with experience in Dash, data visualization, and machine learning. Passionate about designing systems people actually want to use.",
                                    className="card-text"
                                ),
                                dbc.Button("Read Full Bio", href="/about/andrew", color="primary", className="mt-2")
                            ])
                        ], className="h-100"),
                        width=12, lg=4, className="mb-4"
                    ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Shayan_Akhoondan.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Shayan Akhoondan", className="card-title"),
                                    html.H6("Full Stack Developer", className="card-title"),
                                    html.P(
                                    "Builder of resilient systems with a research interest in AI and security. Contributed to UI design and simulation modeling on CyberGator.",
                                    className="card-text"
                                ),
                                dbc.Button("Read Full Bio", href="/about/shayan", color="primary", className="mt-2")
                            ])
                        ], className="h-100"),
                        width=12, lg=4, className="mb-4"
                    ),
                    ], className="justify-content-center"),  
                ], width=12)
            ], className="mb-5"),  
            
            # ---- Section: Rethinking Vulnerability Prioritization + Strategy Cards ----
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H2("Rethinking Vulnerability Prioritization", className="section-title text-center mt-3 mb-3"),

                            html.P("Modern systems are too complex to secure by patching everything.", className="text-center"),
                            html.P("The critical question isn't which CVEs are most severe:", className="text-center"),
                            html.P("it's which ones expose meaningful paths to compromise.", className="text-center"),
                            html.P("CyberGator enables teams to model real architectures, analyze how vulnerabilities propagate, and identify the attack paths that truly threaten critical functions. It shifts focus from surface-level severity to structural risk.", className="text-center"),

                            html.P("CVSS scores show isolated risk. CyberGator shows connected risk — where system structure, privilege boundaries, and software dependencies all shape exposure.", className="text-center"),
                        ])
                    ], className="mb-4 shadow-sm"),
                    width=8, className="mx-auto"  
                )
            ]),

            dbc.Row([
                dbc.Col([
                    html.H2("Prioritize - Evaluate - Defend", className="section-title text-center mt-4 mb-4"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.Img(src="assets/icon_prioritize.png", height="120px", className="mb-2 d-block mx-auto"),
                                    html.H5("Impact-Based Risk Modeling", className="fw-bold text-center"),
                                    html.P("Focus on vulnerabilities that affect critical functions, not just those with high CVSS scores.", className="text-center")
                                ])
                            ], className="h-100 shadow-sm"),
                            md=4
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.Img(src="assets/icon_attack_path.png", height="120px", className="mb-2 d-block mx-auto"),
                                    html.H5("Attack Path Evaluation", className="fw-bold text-center"),
                                    html.P("Trace how CVEs combine and propagate to form complete chains toward mission-critical assets.", className="text-center")
                                ])
                            ], className="h-100 shadow-sm"),
                            md=4
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardBody([
                                    html.Img(src="assets/icon_resilience_score.png", height="120px", className="mb-2 d-block mx-auto"),
                                    html.H5("System-Wide Defense Planning", className="fw-bold text-center"),
                                    html.P("Use graph-based insights to identify chokepoints, misconfigurations, and strategic hardening opportunities.", className="text-center")
                                ])
                            ], className="h-100 shadow-sm"),
                            md=4
                        )
                    ], className="g-4 justify-content-center")
                ], width=12)
            ], className="mb-5"),
        ], className="d-flex flex-column align-items-center",  # Centers content in the page
        style={"maxWidth": "80%", "margin": "0 auto"})  # Adjusts width and centers
    ])