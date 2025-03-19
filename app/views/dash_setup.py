from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from app.views.pages.auth_layouts import get_auth_layout
from app.views.pages.sidebar import sidebar
from app.views.pages.homepage import homepage_layout
from app.views.pages.sue_graph_layout import sue_graph_layout
from app.views.pages.dashboard import dashboard
from app.views.pages.banner import banner
from app.views.callbacks.sue_graph_callbacks import fetch_data
from app.views.pages.network_graph import graph_layout
from app.views.callbacks.graph_callbacks import register_graph_callbacks
from app.views.pages.system_tables import system_tables_layout
from app.views.pages.cves_table import cves_table_layout
from app.views.pages.nodes_table import nodes_table_layout
from app.views.pages.export_layout import export_layout

def render_page_content(pathname, session_user):
    """Dynamically updates the content area based on the session"""
    if pathname == "/auth":
        if session_user:  # If user is logged in (stored in Dash session), redirect to welcome
            return dcc.Location(id="redirect-welcome", href="/welcome", refresh=True)
        return get_auth_layout()
    
    # elif pathname == "/register":
    #     if session_user:  # If user is logged in, redirect to the welcome page
    #         return dcc.Location(id="redirect-welcome", href="/welcome", refresh=True)
    #     return register_layout()
    elif pathname == "/welcome":
        # if not session_user:  # If no session, redirect back to login
        #     return dcc.Location(id="redirect-auth", href="/auth", refresh=True)
        # return html.H1(f"Welcome {session_user}! You are logged in.")
        return homepage_layout()
    elif pathname == "/dashboard":
        if not session_user:
            return dbc.Container([
                dbc.Row(dbc.Col(html.H1("Access Denied", className="text-center mt-4"))),
                dbc.Row(dbc.Col(html.P("You must be logged in to view this page.", className="text-center"))),
                dcc.Link('Go to Login Page', href='/auth', className="btn btn-link d-block text-center"),
            ], fluid=True)
        return dashboard(session_user)
    elif pathname == "/sue-graph":
        print(fetch_data(None, "/sue-graph"))
        return sue_graph_layout()
    elif pathname == "/system-graph":
        return graph_layout()
    elif pathname == "/system-tables":
        return system_tables_layout()
    elif pathname == "/system-tables/cves":
        return cves_table_layout()
    elif pathname == "/system-tables/nodes":
        return nodes_table_layout()
    elif pathname == "/export":
        return export_layout()  # This will call the layout for the export page.



    
    return html.H1("404 - Page Not Found", className="text-center")


def get_main_layout():
    return html.Div([
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="session-user", storage_type="session"), 
        html.Div(id="sidebar-container"), 
        html.Div(id="banner-container"), 
        html.Div(id="page-content",
                style={"marginLeft": "15%", "marginTop": "80px", "padding": "20px"})
    ])

@callback(Output("page-content", "children"), [Input("url", "pathname"), State("session-user", "data")])
def update_page(pathname, session_user):
    return render_page_content(pathname, session_user)


@callback(Output("banner-container", "children"), [Input("session-user", "data")])
def update_banner(session_user):
    return banner(session_user=session_user)

@callback(Output("sidebar-container", "children"), [Input("session-user", "data")])
def update_sidebar(session_user):
    return sidebar(session_user=session_user)