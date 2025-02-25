from dash import html
import dash_bootstrap_components as dbc


def homepage_layout():
    return dbc.Container([
    dbc.Row(dbc.Col(html.H1("Homepage", className="text-center mt-4"))),
    dbc.Row(dbc.Col(html.P("Welcome to the Homepage!", className="text-center"))),
    
    # Add the image
    dbc.Row(dbc.Col(
        html.Img(src="/assets/Mypicture.jpg", style={"width": "100%", "maxWidth": "300px", "display": "block", "marginLeft": "auto", "marginRight": "auto"}),
        className="text-center"  # Center the image
    )),
    
    # Add a paragraph underneath the image
    dbc.Row(dbc.Col(
        html.P("This is a picture of me!", className="text-center mt-3"),
        className="text-center"  # Center the paragraph
    )),
    dbc.Row(dbc.Col(
        html.Img(src="/assets/Mypicture.jpg", style={"width": "100%", "maxWidth": "300px", "display": "block", "marginLeft": "auto", "marginRight": "auto"}),
        className="text-center"  # Center the image
    )),
    
    # Add a paragraph underneath the image
    dbc.Row(dbc.Col(
        html.P("This is a picture of me!", className="text-center mt-3"),
        className="text-center"  # Center the paragraph
    )),
    dbc.Row(dbc.Col(
        html.Img(src="/assets/Mypicture.jpg", style={"width": "100%", "maxWidth": "300px", "display": "block", "marginLeft": "auto", "marginRight": "auto"}),
        className="text-center"  # Center the image
    )),
    
    # Add a paragraph underneath the image
    dbc.Row(dbc.Col(
        html.P("This is a picture of me!", className="text-center mt-3"),
        className="text-center"  # Center the paragraph
    )),
    dbc.Row(dbc.Col(
        html.Img(src="/assets/Mypicture.jpg", style={"width": "100%", "maxWidth": "300px", "display": "block", "marginLeft": "auto", "marginRight": "auto"}),
        className="text-center"  # Center the image
    )),
    
    # Add a paragraph underneath the image
    dbc.Row(dbc.Col(
        html.P("This is a picture of me!", className="text-center mt-3"),
        className="text-center"  # Center the paragraph
    )),
    dbc.Row(dbc.Col(
        html.Img(src="/assets/Mypicture.jpg", style={"width": "100%", "maxWidth": "300px", "display": "block", "marginLeft": "auto", "marginRight": "auto"}),
        className="text-center"  # Center the image
    )),
    
    # Add a paragraph underneath the image
    dbc.Row(dbc.Col(
        html.P("This is a picture of me!", className="text-center mt-3"),
        className="text-center"  # Center the paragraph
    )),
], fluid=True)