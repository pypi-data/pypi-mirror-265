from __future__ import annotations

from pathlib import Path
from unittest import TestCase

import jsonschema

from fabsync.config import ConfigError, SyncConfig


try:
    import tomllib as toml  # type: ignore[import]
except ModuleNotFoundError:
    import tomli as toml


class ConfigTestCase(TestCase):
    def test_absent(self):
        config = self.load("absent")

        self.assertEqual(config.name, "absent")
        self.assertEqual(config.files, {})
        self.assertEqual(config.defaults, SyncConfig.root().defaults)

    def test_empty(self):
        config = self.load("empty")

        self.assertEqual(config.name, "empty")
        self.assertEqual(config.files, {})
        self.assertEqual(config.defaults, SyncConfig.root().defaults)

    def test_toml_error(self):
        with self.assertRaises(ConfigError) as cm:
            self.load("toml_error")

        self.assertIsInstance(cm.exception.__cause__, toml.TOMLDecodeError)

    def test_schema_error(self):
        with self.assertRaises(ConfigError) as cm:
            self.load("schema_error")

        self.assertIsInstance(cm.exception.__cause__, jsonschema.ValidationError)

    def test_complete(self):
        """Typical values don't throw errors."""
        self.load("complete")

    def test_tags(self):
        """Tags are inherited correctly."""
        config = self.load("tags")

        self.assertEqual(config.dir_opts().tags, {"a", "b", "dir"})
        self.assertEqual(config.file_opts("one").tags, {"b", "f1"})
        self.assertEqual(config.file_opts("two").tags, {"a", "b", "f2"})
        self.assertEqual(config.file_opts("three").tags, {"f3"})

    def test_tags2(self):
        """Tags are inherited correctly."""
        config = self.load("tags2")

        self.assertEqual(config.dir_opts().tags, {"dir"})
        self.assertEqual(config.file_opts("one").tags, {"file"})

    def test_vars(self):
        """Render vars are inherited correcly."""
        config = self.load('vars')

        self.assertEqual(config.dir_opts().vars, {})
        self.assertEqual(config.file_opts('one').vars, {'a': 'a', 'b': 'b'})
        self.assertEqual(config.file_opts('two').vars, {'a': 'a', 'b': 'B', 'c': 'C'})

    #
    # Utils
    #

    def load(self, name: str) -> SyncConfig:
        path = self.root(name)
        base = SyncConfig.root()

        return SyncConfig.load(path, base.defaults)

    def root(self, name: str) -> Path:
        return Path(__file__).parent / "config" / name
