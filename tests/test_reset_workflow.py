"""Regression checks for restoring edited sample data and the Reset All callback."""
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from dash import Dash, no_update
from dash.exceptions import PreventUpdate

from app.services import data_loader
from app.services.node_service import remove_node_from_system_graph
from app.services.reset_service import reset_all_data, JSON_BACKUPS, CSV_BACKUPS
from app.views.callbacks.reset_callbacks import register_reset_callbacks


class ResetDataTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name) / "data"
        shutil.copytree(Path(__file__).parents[1] / "app/data", root)
        self.root = root
        self.json_path = root / "json"
        self.csv_path = root / "csv"
        self.backup_path = root / "backup"
        for key, value in (("DATA_PATH", self.json_path), ("CSV_PATH", self.csv_path),
                           ("BACKUP_PATH", self.backup_path)):
            context = patch.object(data_loader, key, str(value))
            context.start()
            self.addCleanup(context.stop)
        self.nodes = json.loads((self.backup_path / "Nodes_Complete.json").read_text())

    def live_inputs(self):
        return {(self.json_path / name): (self.json_path / name).read_bytes() for name in JSON_BACKUPS} | {
            (self.csv_path / name): (self.csv_path / name).read_bytes() for name in CSV_BACKUPS}

    def test_delete_recalculate_reset_restores_inputs_scores_and_repeat_reset(self):
        from app.services import resilience_score_calculator as calculator
        baseline = reset_all_data()
        for _ in range(2):
            removed = self.nodes[0]["node_id"]
            remove_node_from_system_graph(removed)
            changed = data_loader.get_nodes()
            self.assertEqual(len(changed), len(self.nodes) - 1)
            changed_graph = calculator.G.copy()
            changed_scores = calculator.calculate_resilience_scores(
                changed, changed_graph, calculator.environmental_risk_scores_fuzzy,
                calculator.critical_function_weights)
            self.assertNotEqual(calculator.calculate_system_resilience(changed_scores),
                                baseline["system_resilience_score"])

            result = reset_all_data()
            self.assertEqual(result, baseline)
            for name in JSON_BACKUPS:
                self.assertEqual((self.json_path / name).read_bytes(),
                                 (self.backup_path / name).read_bytes(), name)
            for name in CSV_BACKUPS:
                self.assertEqual((self.csv_path / name).read_bytes(),
                                 (self.backup_path / name).read_bytes(), name)
            saved = json.loads((self.json_path / "output/System_Resilience_Scores.json").read_text())
            self.assertEqual(saved["system_resilience_score"], baseline["system_resilience_score"])
            self.assertEqual({n["node_id"] for n in saved["individual_node_scores"]},
                             {n["node_id"] for n in self.nodes})
            metrics = json.loads((self.json_path / "output/Individual_Node_Metrics.json").read_text())
            self.assertEqual(len(metrics), len(self.nodes))

    def test_missing_backup_does_not_partially_restore_inputs(self):
        remove_node_from_system_graph(self.nodes[0]["node_id"])
        before = self.live_inputs()
        (self.backup_path / CSV_BACKUPS[-1]).unlink()
        with self.assertRaises(FileNotFoundError):
            reset_all_data()
        self.assertEqual(self.live_inputs(), before)

    def test_invalid_json_backup_does_not_partially_restore_inputs(self):
        remove_node_from_system_graph(self.nodes[0]["node_id"])
        before = self.live_inputs()
        (self.backup_path / JSON_BACKUPS[-1]).write_text("invalid json")
        with self.assertRaises(json.JSONDecodeError):
            reset_all_data()
        self.assertEqual(self.live_inputs(), before)

    def test_reset_refreshes_simulation_inputs_loaded_before_reset(self):
        from app.services import constraints
        from app.views.pages import apt_simulation
        changed = self.nodes[1:]
        with patch.object(constraints, "NODES_DATA", changed), \
             patch.object(constraints, "PRIVILEGE_LOOKUP", {}), \
             patch.object(apt_simulation, "NODES_DATA", changed), \
             patch.object(apt_simulation, "PRIVILEGE_LOOKUP", {}):
            reset_all_data()
            graph, _ = apt_simulation.load_sim_system_graph(None)
            node_ids = {entry["data"]["id"] for entry in graph if "id" in entry["data"]}
            self.assertEqual(node_ids, {node["node_id"] for node in self.nodes})
            self.assertIn(self.nodes[0]["node_id"], constraints.PRIVILEGE_LOOKUP)


class ResetCallbackTests(unittest.TestCase):
    def setUp(self):
        app = Dash("reset_callback_test")
        register_reset_callbacks(app)
        self.callback = next(iter(app.callback_map.values()))["callback"].__wrapped__

    def test_initial_layout_does_not_reset_data(self):
        with patch("app.views.callbacks.reset_callbacks.reset_all_data") as reset:
            with self.assertRaises(PreventUpdate):
                self.callback(0, "/dashboard")
            reset.assert_not_called()

    def test_success_reloads_the_current_page(self):
        with patch("app.views.callbacks.reset_callbacks.reset_all_data") as reset:
            href, message = self.callback(1, "/system-graph")
            reset.assert_called_once()
            self.assertTrue(href.startswith("/system-graph?reset="))
            self.assertIs(message, no_update)

    def test_failure_displays_feedback_without_reloading(self):
        with patch("app.views.callbacks.reset_callbacks.reset_all_data",
                   side_effect=OSError("test failure")), \
             self.assertLogs("app.views.callbacks.reset_callbacks", level="ERROR"):
            href, message = self.callback(1, "/dashboard")
            self.assertIs(href, no_update)
            self.assertIn("Reset failed", message)


if __name__ == "__main__":
    unittest.main()
