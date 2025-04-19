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
from app.controllers.cve_controller import cve_bp

from app.views.dash_setup import get_main_layout
import app.views.callbacks.auth_callbacks
from app.controllers.graph_controller import graph_bp
from app.views.callbacks.graph_callbacks import register_graph_callbacks
from app.views.callbacks.system_tables_callbacks import register_system_tables_callbacks
from app.controllers.resilience_controller import resilience_bp
from app.controllers.software_controller import software_bp
from app.views.callbacks.resilience_callbacks import register_resilience_callbacks
from app.controllers.nodes_controller import nodes_bp
from app.views.callbacks.neo4j_callbacks import register_neo4j_callbacks
from app.views.callbacks.node_callbacks import register_node_callbacks
from app.views.callbacks.edge_callbacks import register_edge_callbacks
from app.views.callbacks.export_callbacks import register_export_callbacks
from app.views.callbacks.software_unique_callbacks import register_software_unique_callbacks
from app.views.callbacks.cve_simulation_callbacks import register_cve_simulation_callbacks
from app.controllers.neo4j_controller import neo4j_bp

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
flask_app.register_blueprint(resilience_bp, url_prefix="/api/resilience")
flask_app.register_blueprint(cve_bp, url_prefix="/api/cve")
flask_app.register_blueprint(nodes_bp, url_prefix="/api/nodes") 
flask_app.register_blueprint(software_bp, url_prefix="/api/software")
flask_app.register_blueprint(neo4j_bp, url_prefix="/api/neo4j")

# Dash configs
dash_app = Dash(__name__, server=flask_app, url_base_pathname="/", suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.layout = get_main_layout()

atexit.register(close_pool)
atexit.register(close_neo4j_connection)

register_graph_callbacks(dash_app)
register_system_tables_callbacks(dash_app)
register_resilience_callbacks(dash_app)  # Register the resilience score callback
register_neo4j_callbacks(dash_app)
register_node_callbacks(dash_app)
register_edge_callbacks(dash_app)
register_export_callbacks(dash_app)
register_software_unique_callbacks(dash_app)
register_cve_simulation_callbacks(dash_app)

# Run Flask & Dash
if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=8000)
