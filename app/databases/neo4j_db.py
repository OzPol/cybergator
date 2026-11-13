"""Optional Neo4j connection, created only when an enabled feature is used."""
import logging
import os
from threading import Lock

from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
neo4j_driver = None
_driver_lock = Lock()


class Neo4jUnavailable(RuntimeError):
    """The optional graph backend is disabled, unconfigured or unreachable."""


def neo4j_enabled():
    return os.getenv("NEO4J_ENABLED", "false").strip().lower() in {"true", "1", "yes"}


def get_neo4j_connection():
    global neo4j_driver
    if not neo4j_enabled():
        raise Neo4jUnavailable("Neo4j is disabled. The JSON System Graph remains available.")
    uri = os.getenv("NEO4J_URI", "").strip()
    user = os.getenv("NEO4J_USER", "").strip()
    password = os.getenv("NEO4J_PASSWORD", "")
    if not all((uri, user, password)):
        raise Neo4jUnavailable("Neo4j configuration is incomplete.")
    with _driver_lock:
        if neo4j_driver is not None:
            return neo4j_driver
        try:
            from neo4j import GraphDatabase
        except ImportError:
            raise Neo4jUnavailable("Install the neo4j extra to enable this backend.") from None
        candidate = None
        try:
            candidate = GraphDatabase.driver(
                uri, auth=(user, password), connection_timeout=5,
                connection_acquisition_timeout=5, max_transaction_retry_time=5,
            )
            candidate.verify_connectivity()
        except Exception:
            if candidate is not None:
                candidate.close()
            # Driver exceptions may include connection details; do not expose them.
            logger.warning("Neo4j connection failed.")
            raise Neo4jUnavailable("Neo4j is unavailable. Check its configuration and service status.") from None
        neo4j_driver = candidate
        return neo4j_driver


def run_query(query, parameters=None):
    driver = get_neo4j_connection()
    try:
        from neo4j import Query
        with driver.session() as session:
            return session.run(Query(query, timeout=10), parameters or {}).data()
    except Exception:
        raise Neo4jUnavailable("The Neo4j query could not be completed.") from None


def close_neo4j_connection():
    global neo4j_driver
    with _driver_lock:
        if neo4j_driver is not None:
            neo4j_driver.close()
            neo4j_driver = None
