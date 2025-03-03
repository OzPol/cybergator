
from dash import dcc, html

def sue_graph_layout():
    return html.Div([
        html.H1("Sue Graph Viewer"),
        dcc.Store(id="graph-trigger", data={"refresh": True}), 
        html.Img(id="graph-visualization", src="/assets/system_graph.png", 
                 style={"width": "100%"}),  
    ])
