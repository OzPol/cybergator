import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("SUPABASE_DB_URL")

# Initialize the connection pool at startup
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,  
        maxconn=10, 
        dsn=POSTGRES_URL
    )
    if connection_pool:
        print("✅ PostgreSQL Connection Pool Created Successfully!")
except psycopg2.Error as e:
    print("❌ Error Creating Connection Pool:", e)
    connection_pool = None 

def get_sql_connection():
    """Fetches a connection from the pool."""
    try:
        if connection_pool:
            conn = connection_pool.getconn()
            print("✅ Supabase Connection Pool Opened.")
            return conn
        else:
            print("❌ Connection Pool is not initialized.")
            return None
    except psycopg2.Error as e:
        print("❌ Error getting connection:", e)
        return None

def release_connection(conn):
    """Releases a connection back to the pool."""
    try:
        if connection_pool and conn:
            connection_pool.putconn(conn)
    except psycopg2.Error as e:
        print("❌ Error releasing connection:", e)

def close_pool():
    """Closes all connections in the pool (call this on shutdown)."""
    try:
        if connection_pool:
            connection_pool.closeall()
    except psycopg2.Error as e:
        print("❌ Error closing connection pool:", e)
