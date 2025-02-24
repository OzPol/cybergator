from os import getenv
from dash import Dash, html
from flask import Flask
from dotenv import load_dotenv

from app.databases.psql_db import get_sql_connection
from app.databases.neo4j_db import get_neo4j_connection

from app.controllers.auth_controller import auth_bp

load_dotenv()

# Flask configs
flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY")
flask_app.config["SESSION_TYPE"] = getenv("SESSION_TYPE")
flask_app.config["SESSION_PERMANENT"] = getenv("SESSION_PERMANENT")
flask_app.config["SESSION_USE_SIGNER"] = getenv("SESSION_USE_SIGNER")

# API route registration
flask_app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Initialize Dash inside Flask
dash_app = Dash(__name__, server=flask_app, url_base_pathname="/")

# Test databases
get_sql_connection()
get_neo4j_connection()

# Test Dash Layout
dash_app.layout = html.Div([
    html.H1("Database Connection Test"),
])
    
# Run Flask & Dash
if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=8000)
