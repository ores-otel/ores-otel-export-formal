"""Traversal/symlink escape guards for the fmctl model manifest."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_manifest as validator


class ManifestSpecTests(unittest.TestCase):
    def test_current_manifest_points_to_repo_owned_spec(self):
        import tomllib
        data = tomllib.loads(validator.MANIFEST.read_text())
        spec = validator.safe_spec_path(data["spec"])
        self.assertTrue(spec.is_file())
        self.assertTrue(spec.is_relative_to(validator.ROOT.resolve()))

    def test_rejects_malformed_and_traversal_paths(self):
        for value in [None, 12, "", "/etc/passwd", "../secret",
                      "formal/../../secret", "formal//model.qnt",
                      "./formal/model.qnt", "formal\\\\model.qnt"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validator.safe_spec_path(value)

    def test_rejects_external_symlink(self):
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as outside:
            root = Path(repo)
            (root / "formal").mkdir()
            external = Path(outside) / "private.qnt"
            external.write_text("private")
            (root / "formal" / "linked.qnt").symlink_to(external)
            with patch.object(validator, "ROOT", root), self.assertRaises(ValueError):
                validator.safe_spec_path("formal/linked.qnt")


if __name__ == "__main__":
    unittest.main()
