from os import getenv
from dash import Dash
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import atexit
import dash_bootstrap_components as dbc


from application.databases.psql_db import close_pool
from application.databases.neo4j_db import close_neo4j_connection

from application.controllers.auth_controller import auth_bp
from application.views.dash_setup import get_main_layout
import application.views.callbacks.auth_callbacks