"""Render the legacy static system graph without raster imaging dependencies."""
from pathlib import Path
from tempfile import NamedTemporaryFile
from xml.etree import ElementTree as ET

import networkx as nx


def generate_graph_system(json_data, output_dir=None):
    """Save an SVG graph and return its path; ElementTree escapes XML labels."""
    if not json_data:
        return None
    graph = nx.Graph()
    nodes = {str(node["node_id"]): node for node in json_data}
    graph.add_nodes_from(nodes)
    for node_id, node in nodes.items():
        graph.add_edges_from((node_id, str(other)) for other in node.get("connected_to", []))

    positions = nx.spring_layout(graph, seed=10, k=0.2)
    points = {node: (720 + float(pos[0]) * 620, 420 + float(pos[1]) * 320)
              for node, pos in positions.items()}
    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", viewBox="0 0 1440 800",
                     role="img", **{"aria-label": "System Information Architecture Graph"})
    ET.SubElement(svg, "rect", width="1440", height="800", fill="white")
    title = ET.SubElement(svg, "text", x="720", y="35", fill="black",
                          **{"text-anchor": "middle", "font-size": "24"})
    title.text = "System Information Architecture Graph"
    for first, second in graph.edges:
        x1, y1 = points[first]
        x2, y2 = points[second]
        ET.SubElement(svg, "line", x1=str(x1), y1=str(y1), x2=str(x2), y2=str(y2),
                      stroke="#888", **{"stroke-width": "1.5"})
    for node_id, (x, y) in points.items():
        node = nodes.get(node_id, {})
        if node.get("node_type") in ("Switch", "Firewall", "Router"):
            ET.SubElement(svg, "rect", x=str(x - 20), y=str(y - 20), width="40", height="40",
                          fill="lightblue", stroke="#333")
        else:
            ET.SubElement(svg, "circle", cx=str(x), cy=str(y), r="18",
                          fill="lightgreen", stroke="#333")
        label = ET.SubElement(svg, "text", x=str(x), y=str(y + 36), fill="black",
                              **{"text-anchor": "middle", "font-size": "12"})
        label.text = str(node.get("node_name", node_id) if node.get("node_type") in
                         ("Firewall", "Router") else node_id)

    assets_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parents[2] / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)
    output_path = assets_dir / "system_graph.svg"
    # Atomic replacement avoids partially written images during concurrent requests.
    with NamedTemporaryFile(dir=assets_dir, suffix=".svg", delete=False) as temporary:
        temporary_path = Path(temporary.name)
        ET.ElementTree(svg).write(temporary, encoding="utf-8", xml_declaration=True)
    temporary_path.replace(output_path)
    return str(output_path)
