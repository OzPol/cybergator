import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("SUPABASE_DB_URL")

def get_sql_connection():
    """Creates and returns a new postgres database connection."""
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        print("Connection successful!")
        return conn
    except psycopg2.Error as e:
        print("Database connection error:", e)
        return None