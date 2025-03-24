import json
import os
from neo4j import GraphDatabase

NEO4J_URI = "neo4j+s://92da8f26.databases.neo4j.io"    #    "bolt://localhost:7687"  # Can be changed to Aura or Docker 
USERNAME  = "neo4j"
PASSWORD  = "iwe6XXamOhMLV8Wg_T_7KU34XH4Y01GGea4jLqiJykk"
# PASSWORD  = os.getenv("NEO4J_PASSWORD")


def create_nodes_and_relationships():
    with open("app/data/json/Nodes_Complete.json", "r") as file:
        nodes = json.load(file)

    driver = GraphDatabase.driver(NEO4J_URI, auth=(USERNAME, PASSWORD))

    with driver.session() as session:
        for node in nodes:
            node["CVE_NVD"] = json.dumps(node.get("CVE_NVD", {}))  # Safely default to empty
            query = """
            MERGE (n:Node {node_id: $node_id})
            SET n.node_name = $node_name,
                n.node_type = $node_type,
                n.critical_functions = $critical_functions,
                n.connected_to = $connected_to,
                n.critical_data_stored = $critical_data_stored,
                n.backup_role = $backup_role,
                n.data_redundancy = $data_redundancy,
                n.redundancy = $redundancy,
                n.risk_factor = $risk_factor,
                n.switch_dependency = $switch_dependency,
                n.resilience_penalty = $resilience_penalty,
                n.CVE = $CVE,
                n.CVE_NVD = $CVE_NVD
            """
            session.run(query, **node)

            # Create relationships
            for neighbor in node.get("connected_to", []):
                session.run("""
                    MATCH (a:Node {node_id: $node_id}), (b:Node {node_id: $neighbor_id})
                    MERGE (a)-[:CONNECTED_TO]->(b)
                """, node_id=node["node_id"], neighbor_id=neighbor)

    driver.close()
    print("✅ Neo4j nodes + relationships imported.")