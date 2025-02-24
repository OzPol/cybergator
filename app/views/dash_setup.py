from dash import html, dcc, callback, Output, Input, State
from app.views.pages.auth_layouts import get_auth_layout

def render_page_content(pathname, session_user):
    """Dynamically updates the content area based on the session"""
    if pathname == "/auth":
        if session_user:  # If user is logged in (stored in Dash session), redirect to welcome
            return dcc.Location(id="redirect-welcome", href="/welcome", refresh=True)
        return get_auth_layout()
    
    elif pathname == "/welcome":
        if not session_user:  # If no session, redirect back to login
            return dcc.Location(id="redirect-auth", href="/auth", refresh=True)
        return html.H1(f"Welcome {session_user}! You are logged in.")
    
    return html.H1("404: Page not found")

def get_main_layout():
    return html.Div([
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="session-user", storage_type="session"), 
        html.Div(id="page-content")
    ])

@callback(Output("page-content", "children"), [Input("url", "pathname"), State("session-user", "data")])
def update_page(pathname, session_user):
    return render_page_content(pathname, session_user)
