"""Legacy authentication storage; never connects during module import."""
import logging
import os
from threading import Lock

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
connection_pool = None
_pool_lock = Lock()


def get_sql_connection():
    global connection_pool
    dsn = os.getenv("SUPABASE_DB_URL", "")
    if not dsn:
        return None
    with _pool_lock:
        if connection_pool is None:
            try:
                from psycopg2.pool import ThreadedConnectionPool
                connection_pool = ThreadedConnectionPool(
                    minconn=1, maxconn=10, dsn=dsn, connect_timeout=5
                )
            except Exception:
                logger.warning("Legacy PostgreSQL connection is unavailable.")
                return None
        return connection_pool.getconn()


def release_connection(conn):
    if connection_pool is not None and conn is not None:
        connection_pool.putconn(conn)


def close_pool():
    global connection_pool
    with _pool_lock:
        if connection_pool is not None:
            connection_pool.closeall()
            connection_pool = None
