import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

def get_neo4j_connection():
    """Returns a Neo4j database connection."""
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        driver.verify_connectivity
        print("✅ Neo4j Aura Connection successful!")
        return driver
    except Exception as e:
        print("❌ Neo4j connection error", e)
        return None
    
def run_query(query, parameters=None):
    """Runs a Cypher query and returns results."""
    driver = get_neo4j_connection()
    if driver is None:
        return []

    with driver.session() as session:
        results = session.run(query, parameters).data()
    
    driver.close()
    return results