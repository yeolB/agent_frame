"""Installer ownership and revision regression tests (stdlib only)."""
import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

INSTALLER = Path(__file__).resolve().parents[1] / "install-continuity"
loader = importlib.machinery.SourceFileLoader("installer", str(INSTALLER))
spec = importlib.util.spec_from_loader(loader.name, loader)
installer = importlib.util.module_from_spec(spec)
loader.exec_module(installer)


class InstallationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", str(self.root)], check=True, capture_output=True)

    def run_install(self, *args):
        with patch("sys.argv", [str(INSTALLER), str(self.root), *args]):
            return installer.main()

    def test_update_ownership_and_idempotency(self):
        self.run_install()
        for name in installer.MANAGED_FILE_PATHS:
            (self.root / name).write_text("old AF content", encoding="utf-8")
        project_files = ["GOAL.md", "state/CURRENT.md", "state/cadence.json",
                         "memory/INDEX.md", "state/active/work.md",
                         "memory/records/lesson.md", ".agents/skills/custom/SKILL.md"]
        for name in project_files:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("project-owned", encoding="utf-8")
        agents = self.root / "AGENTS.md"
        agents.write_text("Project rule\n" + agents.read_text(), encoding="utf-8")
        hooks = self.root / ".codex/hooks.json"
        value = json.loads(hooks.read_text())
        custom = {"hooks": [{"type": "command", "command": "echo project"}]}
        value["hooks"]["Stop"].append(custom)
        hooks.write_text(json.dumps(value), encoding="utf-8")
        self.run_install()
        for name in installer.MANAGED_FILE_PATHS:
            self.assertEqual((self.root / name).read_bytes(), (installer.SOURCE_ROOT / name).read_bytes())
        for name in project_files:
            self.assertEqual((self.root / name).read_text(), "project-owned")
        self.assertTrue(agents.read_text().startswith("Project rule\n"))
        self.assertIn(custom, json.loads(hooks.read_text())["hooks"]["Stop"])
        record = self.root / installer.INSTALL_RECORD
        before = record.read_bytes()
        self.assertEqual(json.loads(before)["revision"], installer.source_identity()["revision"])
        self.run_install()
        self.assertEqual(record.read_bytes(), before)

    def test_dry_run_and_preflight_failure_do_not_write(self):
        self.run_install("--dry-run")
        self.assertFalse((self.root / "AGENTS.md").exists())
        self.assertFalse((self.root / installer.INSTALL_RECORD).exists())
        with self.assertRaises(installer.InstallError):
            self.run_install("--agent-limit", "1")
        self.assertFalse((self.root / installer.INSTALL_RECORD).exists())

    def test_failed_update_does_not_advance_record(self):
        self.run_install()
        record = self.root / installer.INSTALL_RECORD
        before = record.read_bytes()
        (self.root / "scripts/continuity").write_text("old")
        with patch.object(installer, "atomic_write", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.run_install()
        self.assertEqual(record.read_bytes(), before)

    @unittest.skipIf(__import__("os").name == "nt", "Symlink privileges vary on Windows")
    def test_symlink_write_is_rejected(self):
        external = self.root / "external"
        external.mkdir()
        (self.root / "scripts").symlink_to(external, target_is_directory=True)
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse((self.root / installer.INSTALL_RECORD).exists())

    def test_unversioned_source_is_not_clean_revision(self):
        with patch.object(installer, "FRAMEWORK_ROOT", self.root):
            identity = installer.source_identity()
        self.assertIsNone(identity["revision"])


if __name__ == "__main__":
    unittest.main()
