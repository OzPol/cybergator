import json
from app.databases.neo4j_db import get_neo4j_connection


def create_nodes_and_relationships():
    with open("app/data/json/Nodes_Complete.json", "r") as file:
        nodes = json.load(file)

    driver = get_neo4j_connection()

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

        # Create relationships after every endpoint has been created.
        for node in nodes:
            for neighbor in node.get("connected_to", []):
                session.run("""
                    MATCH (a:Node {node_id: $node_id}), (b:Node {node_id: $neighbor_id})
                    MERGE (a)-[:CONNECTED_TO]->(b)
                """, node_id=node["node_id"], neighbor_id=neighbor)

    print("✅ Neo4j nodes + relationships imported.")