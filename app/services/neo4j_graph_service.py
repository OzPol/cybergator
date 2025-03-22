import json
import os
from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://92da8f26.databases.neo4j.io"    #    "bolt://localhost:7687"  # Can be changed to Aura or Docker 
USERNAME  = "neo4j"
PASSWORD  = "iwe6XXamOhMLV8Wg_T_7KU34XH4Y01GGea4jLqiJykk"
# PASSWORD  = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(USERNAME, PASSWORD))


def get_network_graph():
    """
    Fetch nodes and relationships from Neo4j for Dash Cytoscape.
    """
    query = """
    MATCH (n)-[r]->(m) 
    RETURN n, r, m 
    LIMIT 100
    """
    with driver.session() as session:
        result = session.run(query)
        elements = []
        seen_nodes = set()

        for record in result:
            n = record["n"]
            m = record["m"]
            r = record["r"]

            node1_id = str(n.get("node_id", n.id))
            node2_id = str(m.get("node_id", m.id))
            relationship_type = r.type if r else "CONNECTED_TO"

            # Add first node
            if node1_id not in seen_nodes:
                elements.append({
                    "data": {
                        "id": node1_id,
                        "label": n.get("node_name", node1_id)
                    },
                    "classes": get_node_class(n.get("node_type"))
                })
                seen_nodes.add(node1_id)

            # Add second node
            if node2_id not in seen_nodes:
                elements.append({
                    "data": {
                        "id": node2_id,
                        "label": m.get("node_name", node2_id)
                    },
                    "classes": get_node_class(m.get("node_type"))
                })
                seen_nodes.add(node2_id)

            # Add edge
            elements.append({
                "data": {
                    "source": node1_id,
                    "target": node2_id,
                    "label": relationship_type
                }
            })

        return elements

def get_node_class(node_type):
    if not node_type:
        return "unknown"

    # Normalize and tokenize node type
    words = node_type.lower().replace("_", " ").replace("-", " ").split()

    if {"san", "archive", "backup"}.issubset(words):
        return "san_archive_backup"
    elif {"san", "archive"}.issubset(words):
        return "san_archive"
    elif "san" in words:
        return "san"
    elif "server" in words:
        return "server"
    elif "workstation" in words:
        return "workstation"
    elif "switch" in words:
        return "switch"
    elif "router" in words:
        return "router"
    elif "firewall" in words:
        return "firewall"

    return "unknown"


if __name__ == "__main__":
    print("Network Graph Elements:")
    print(json.dumps(get_network_graph(), indent=2))
    driver.close()