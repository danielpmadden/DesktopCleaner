"""Tests for the DesktopCleaner module."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import desktop_cleaner


class LoadConfigTests(unittest.TestCase):
    def test_returns_default_when_path_missing(self) -> None:
        config = desktop_cleaner.load_config(None)
        self.assertIn("Documents", config)
        self.assertIn("Shortcuts", config)

    def test_loads_custom_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "config.json"
            cfg_path.write_text(json.dumps({"Spreadsheets": [".csv", "XLSX"]}))

            config = desktop_cleaner.load_config(cfg_path)

        self.assertIn("Spreadsheets", config)
        self.assertEqual({".csv", ".xlsx"}, set(config["Spreadsheets"]))
        self.assertIn("Others", config)


class CleanupDesktopTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.tempdir.name)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_moves_files_and_generates_log(self) -> None:
        sample_file = self.base_path / "report.pdf"
        sample_file.write_text("dummy")

        result = desktop_cleaner.cleanup_desktop(self.base_path)

        documents_folder = self.base_path / "Documents"
        self.assertTrue((documents_folder / sample_file.name).exists())
        self.assertTrue(Path(result["log_path"]).exists())

        log_data = json.loads(Path(result["log_path"]).read_text())
        self.assertEqual(1, len(log_data["entries"]))
        self.assertTrue(log_data["entries"][0]["moved"])

    def test_dry_run_does_not_move_files(self) -> None:
        sample_file = self.base_path / "photo.jpg"
        sample_file.write_text("dummy")

        result = desktop_cleaner.cleanup_desktop(self.base_path, dry_run=True)

        images_folder = self.base_path / "Images"
        self.assertFalse((images_folder / sample_file.name).exists())
        self.assertTrue(sample_file.exists())
        self.assertTrue(result["entries"][0].get("dry_run"))

    def test_skips_shortcuts(self) -> None:
        shortcut = self.base_path / "launch.desktop"
        shortcut.write_text("[Desktop Entry]")

        desktop_cleaner.cleanup_desktop(self.base_path)

        self.assertTrue(shortcut.exists())


class CliTests(unittest.TestCase):
    def test_cli_uses_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            (base / "movie.mkv").write_text("video")
            log_file = base / "custom_log.json"

            with mock.patch("sys.argv", ["desktop-cleaner", "--path", str(base), "--dry-run", "--log", str(log_file)]):
                exit_code = desktop_cleaner.main()

            self.assertEqual(0, exit_code)
            self.assertTrue(log_file.exists())
            data = json.loads(log_file.read_text())
            self.assertTrue(data["dry_run"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
