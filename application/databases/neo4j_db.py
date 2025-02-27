import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Create a global driver object for connection pooling
try:
    neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    neo4j_driver.verify_connectivity()
    print("✅ Neo4j Aura Connection Pool Created Successfully!")
except Exception as e:
    print("❌ Neo4j connection error:", e)
    neo4j_driver = None  

def get_neo4j_connection():
    """Returns the Neo4j driver (pooled connection)."""
    if neo4j_driver:
        return neo4j_driver
    print("❌ Neo4j connection unavailable.")
    return None
    
def run_query(query, parameters=None):
    """Runs a Cypher query and returns results."""
    driver = get_neo4j_connection()
    if driver is None:
        return []

    with driver.session() as session:
        try:
            results = session.run(query, parameters).data()
            return results
        except Exception as e:
            print("❌ Neo4j Query Error:", e)
            return []

def close_neo4j_connection():
    """Closes the Neo4j driver (call this on shutdown)."""
    global neo4j_driver
    if neo4j_driver:
        neo4j_driver.close()