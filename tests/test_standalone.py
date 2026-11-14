"""Regression checks for the database-free sample-data demo."""
import importlib.util
import os
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, mock_open, patch
from xml.etree import ElementTree as ET

from app.databases.neo4j_db import Neo4jUnavailable, get_neo4j_connection
from app.utils.generate_sue_graph import generate_graph_system


class StandaloneAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = runpy.run_path(str(Path(__file__).parents[1] / "app.py"),
                                   run_name="cybergator_test_entry")
        cls.app = cls.module["flask_app"]
        cls.client = cls.app.test_client()

    def test_health_and_sample_apis_without_credentials(self):
        for path in ("/healthz", "/_dash-layout", "/_dash-dependencies",
                     "/api/graph", "/api/resilience", "/api/sue-graph/"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIsNotNone(response.get_json())
        self.assertFalse(self.app.debug)

    def test_account_routes_are_not_registered(self):
        self.assertFalse(any(rule.rule.startswith("/api/auth")
                             for rule in self.app.url_map.iter_rules()))
        self.assertNotEqual(self.client.post("/api/auth/login", json={}).status_code, 200)

    def test_missing_neo4j_does_not_break_demo(self):
        with patch.dict(os.environ, {"NEO4J_ENABLED": "false"}):
            response = self.client.post("/api/neo4j/import")
            self.assertEqual(response.status_code, 503)
            self.assertIn("disabled", response.get_json()["error"])

    def test_demo_navigation_does_not_require_client_identity(self):
        from app.views.dash_setup import update_sidebar, render_page_content
        with patch.dict(os.environ, {"NEO4J_ENABLED": "false"}):
            sidebar = str(update_sidebar(None).to_plotly_json())
            self.assertIn("/dashboard", sidebar)
            self.assertNotIn("Login/Register", sidebar)
            self.assertNotIn("/neo4j-graph", sidebar)
            self.assertIn("disabled", str(render_page_content("/neo4j-graph", None).to_plotly_json()))

    def test_pillow_and_matplotlib_are_not_installed(self):
        for name in ("PIL", "matplotlib"):
            self.assertIsNone(importlib.util.find_spec(name), name)


class OptionalBackendTests(unittest.TestCase):
    def test_disabled_backend_never_attempts_a_connection(self):
        with patch.dict(os.environ, {"NEO4J_ENABLED": "false"}), \
             patch("socket.create_connection") as connect:
            with self.assertRaisesRegex(Neo4jUnavailable, "disabled"):
                get_neo4j_connection()
            connect.assert_not_called()

    def test_enabled_backend_requires_configuration(self):
        with patch.dict(os.environ, {"NEO4J_ENABLED": "true", "NEO4J_URI": "",
                                    "NEO4J_USER": "", "NEO4J_PASSWORD": ""}):
            with self.assertRaisesRegex(Neo4jUnavailable, "incomplete"):
                get_neo4j_connection()

    def test_connection_failure_does_not_disclose_credentials(self):
        from app.databases import neo4j_db
        fake = MagicMock()
        candidate = fake.GraphDatabase.driver.return_value
        candidate.verify_connectivity.side_effect = RuntimeError("sensitive-test-marker")
        with patch.dict(os.environ, {"NEO4J_ENABLED": "true", "NEO4J_URI": "bolt://example",
                                    "NEO4J_USER": "test", "NEO4J_PASSWORD": "sensitive-test-marker"}), \
             patch.dict("sys.modules", {"neo4j": fake}), \
             patch.object(neo4j_db, "neo4j_driver", None):
            with self.assertRaises(Neo4jUnavailable) as error:
                get_neo4j_connection()
            self.assertNotIn("sensitive-test-marker", str(error.exception))
            candidate.close.assert_called_once()

    def test_import_creates_all_nodes_before_relationships(self):
        import json
        from app.services.neo4j_importer import create_nodes_and_relationships
        driver = MagicMock()
        session = driver.session.return_value.__enter__.return_value
        nodes = [{"node_id": "a", "connected_to": ["b"]},
                 {"node_id": "b", "connected_to": []}]
        with patch("app.services.neo4j_importer.get_neo4j_connection", return_value=driver), \
             patch("builtins.open", mock_open(read_data=json.dumps(nodes))):
            create_nodes_and_relationships()
        queries = [call.args[0] for call in session.run.call_args_list]
        self.assertEqual(len(queries), 3)
        self.assertIn("MERGE (n:Node", queries[0])
        self.assertIn("MERGE (n:Node", queries[1])
        self.assertIn("CONNECTED_TO", queries[2])

    def test_graph_conversion_preserves_types_and_deduplicates_nodes(self):
        from app.services.neo4j_graph_service import get_network_graph
        row = {"n": {"node_id": "a", "node_type": "Firewall"},
               "n_id": "1", "m": {"node_id": "b", "node_type": "Server"},
               "m_id": "2", "relationship_type": "CONNECTED_TO"}
        with patch("app.services.neo4j_graph_service.run_query", return_value=[row, row]):
            elements = get_network_graph()
        nodes = [e for e in elements if "id" in e["data"]]
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0]["classes"], "firewall")


class SvgGraphTests(unittest.TestCase):
    def test_svg_has_edges_and_escaped_labels_without_raster_dependencies(self):
        data = [{"node_id": "a", "node_name": "<script>alert(1)</script>",
                 "node_type": "Router", "connected_to": ["b"]},
                {"node_id": "b", "node_name": "Host", "node_type": "Server"}]
        with TemporaryDirectory() as directory:
            path = generate_graph_system(data, output_dir=directory)
            root = ET.parse(path).getroot()
            ns = {"svg": "http://www.w3.org/2000/svg"}
            self.assertEqual(len(root.findall("svg:line", ns)), 1)
            self.assertEqual(len(root.findall("svg:circle", ns)), 1)
            self.assertEqual(root.findall(".//svg:script", ns), [])
            self.assertIn("&lt;script&gt;", Path(path).read_text())

    def test_empty_data(self):
        self.assertIsNone(generate_graph_system([]))


if __name__ == "__main__":
    unittest.main()
