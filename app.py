import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div("Hello, World!")

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8000)

