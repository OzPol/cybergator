from app.databases.neo4j_db import run_query


def get_network_graph():
    """Fetch bounded graph data through the shared optional Neo4j connection."""
    rows = run_query("""
        MATCH (n)-[r]->(m)
        RETURN properties(n) AS n, elementId(n) AS n_id,
               properties(m) AS m, elementId(m) AS m_id,
               type(r) AS relationship_type
        LIMIT 100
    """)
    elements = []
    seen_nodes = set()
    for record in rows:
        ids = []
        for key in ("n", "m"):
            node = record[key]
            node_id = str(node.get("node_id", record[key + "_id"]))
            ids.append(node_id)
            if node_id not in seen_nodes:
                elements.append({"data": {"id": node_id, "label": node.get("node_name", node_id)},
                                 "classes": get_node_class(node.get("node_type"))})
                seen_nodes.add(node_id)
        elements.append({"data": {"source": ids[0], "target": ids[1],
                                  "label": record["relationship_type"]}})
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
