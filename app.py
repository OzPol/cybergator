from os import getenv
from dash import Dash
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import atexit
import dash_bootstrap_components as dbc


from app.databases.psql_db import close_pool
from app.databases.neo4j_db import close_neo4j_connection

from app.controllers.auth_controller import auth_bp
from app.controllers.sue_graph_controller import sue_bp

from app.views.dash_setup import get_main_layout
import app.views.callbacks.auth_callbacks
from app.controllers.graph_controller import graph_bp
from app.views.callbacks.graph_callbacks import register_graph_callbacks
from app.views.callbacks.system_tables_callbacks import register_system_tables_callbacks


load_dotenv()

# Flask configs
flask_app = Flask(__name__)
flask_app.config["SECRET_KEY"] = getenv("SECRET_KEY")
flask_app.config["SESSION_TYPE"] = getenv("SESSION_TYPE")
flask_app.config["SESSION_PERMANENT"] = getenv("SESSION_PERMANENT")
flask_app.config["SESSION_USE_SIGNER"] = getenv("SESSION_USE_SIGNER")

CORS(flask_app, resources={r"/api/*": {"origins": "*"}})

# API route registration
flask_app.register_blueprint(auth_bp, url_prefix="/api/auth")
flask_app.register_blueprint(sue_bp, url_prefix="/api/sue-graph")
flask_app.register_blueprint(graph_bp, url_prefix="/api/graph")

# Dash configs
dash_app = Dash(__name__, server=flask_app, url_base_pathname="/", suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.layout = get_main_layout()

atexit.register(close_pool)
atexit.register(close_neo4j_connection)

register_graph_callbacks(dash_app)
register_system_tables_callbacks(dash_app)

# Run Flask & Dash
if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=8000)
