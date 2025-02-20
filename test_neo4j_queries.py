import json
import os
from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://92da8f26.databases.neo4j.io"    #    "bolt://localhost:7687"  # Can be changed to Aura or Docker 
USERNAME  = "neo4j"
PASSWORD  = "iwe6XXamOhMLV8Wg_T_7KU34XH4Y01GGea4jLqiJykk"
# PASSWORD  = os.getenv("NEO4J_PASSWORD")
"""
try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(USERNAME, PASSWORD))
    with driver.session() as session:
        result = session.run("MATCH (n) RETURN count(n) AS node_count")
        for record in result:
            print(f"Connected! Nodes in DB: {record['node_count']}")
    driver.close()
except Exception as e:
    print(f"Connection failed: {e}")
"""


driver = GraphDatabase.driver(NEO4J_URI, auth=(USERNAME, PASSWORD))

def get_network_graph():
    """Fetches nodes and relationships from Neo4j for visualization in Dash-Cytoscape."""
    query = """
    MATCH (n)-[r]->(m) 
    RETURN n, r, m 
    LIMIT 100
    """
    with driver.session() as session:
        result = session.run(query)
        elements = []
        seen_nodes = set()  # Avoid duplicate nodes

        for record in result:
            n = record["n"]
            m = record["m"]
            r = record["r"]

            # Ensure nodes have a unique ID
            node1_id = str(n["node_id"])
            node2_id = str(m["node_id"])
            relationship_type = r.type if r.type else "CONNECTED_TO"

            # Add first node if not already added
            if node1_id not in seen_nodes:
                elements.append({
                    "data": {"id": node1_id, "label": n["node_name"]},
                    "classes": "server" if n["node_type"] == "Server" else "device"
                })
                seen_nodes.add(node1_id)

            # Add second node if not already added
            if node2_id not in seen_nodes:
                elements.append({
                    "data": {"id": node2_id, "label": m["node_name"]},
                    "classes": "server" if m["node_type"] == "Server" else "device"
                })
                seen_nodes.add(node2_id)

            # Add relationship (edge)
            elements.append({
                "data": {"source": node1_id, "target": node2_id, "label": relationship_type}
            })

        return elements

if __name__ == "__main__":
    print("Network Graph:", get_network_graph())