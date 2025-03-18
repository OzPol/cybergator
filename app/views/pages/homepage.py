from dash import html
import dash_bootstrap_components as dbc

def homepage_layout():
    return html.Div([  
        dbc.Container([  # Wrapped everything in a centered container
            # Introduction Section
            dbc.Row([  
                dbc.Col([  
                    html.H2("Introduction", className="section-title mb-2 text-center"),
                    html.P("This introduces our work and describes the project in detail",
                           className="mb-5 text-center")
                ], width=12)
            ], className="mt-4 mb-5"),  

            # Meet Our Team Section
            dbc.Row([  
                dbc.Col([  
                    html.H2("Meet Our Team", className="section-title mb-2 text-center"),
                    html.P("Introduce the Members of Our Team", className="section-subtitle mb-4 text-center"),

                    # First Row: 3 Team Cards
                    dbc.Row([  
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Ozlem_Polat.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Name - Role", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Samson_Carter.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Introduce the Members of Our Team", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Jess_Lourenco.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Title", className="card-title"),
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
                                    html.H4("Title", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="assets/Shayan_Akhoondan.jpg", top=True, className="team-card-img"),
                                dbc.CardBody([
                                    html.H4("Title", className="card-title"),
                                    html.P("Body text for whatever you'd like to say.", className="card-text")
                                ])
                            ], className="h-100"),
                            width=12, lg=4, className="mb-4"
                        ),
                    ], className="justify-content-center"),  
                ], width=12)
            ], className="mb-5"),  

            # How to Use the App Section
            dbc.Row([  
                dbc.Col([  
                    html.H2("How to Use the App", className="section-title mb-2 text-center"),
                    html.P("Detailed Instructions for User Reference", className="section-subtitle mb-3 text-center"),
                    html.Div([  
                        html.P("Body text for your whole article or post. We'll put in some lorem ipsum to show how a filled-out page might look."),
                        html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
                    ], className="p-4 border rounded bg-light text-center")
                ], width=12)
            ], className="mb-5"),  

        ], className="d-flex flex-column align-items-center",  # Centers content in the page
        style={"maxWidth": "80%", "margin": "0 auto"})  # Adjusts width and centers
    ])