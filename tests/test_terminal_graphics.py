"""Kitty-graphics detection is decided in one place and from the environment.

`terminal_supports_kitty_graphics()` is what the thumbnail preview, the inline
`--vo=kitty` players and the diagnostics panel consult. These tests are
env-only: no terminal, no image, no subprocess.

Run with:

    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
OMAYT = REPO_ROOT / "omayt"

module = None
_isolated_home: Path | None = None
_env_patch: mock._patch_dict | None = None


def setUpModule() -> None:
    """Import the app with HOME and the XDG dirs redirected.

    The module resolves its cache/config dirs at import time, so the redirect
    has to happen before `exec_module`.
    """
    global module, _isolated_home, _env_patch

    _isolated_home = Path(tempfile.mkdtemp(prefix="omayt-graphics-"))
    isolated = {
        "HOME": str(_isolated_home),
        "XDG_CONFIG_HOME": str(_isolated_home / ".config"),
        "XDG_CACHE_HOME": str(_isolated_home / ".cache"),
        "XDG_DATA_HOME": str(_isolated_home / ".local/share"),
        "XDG_STATE_HOME": str(_isolated_home / ".local/state"),
        "OMAYT_LANG": "en",
    }
    _env_patch = mock.patch.dict(os.environ, isolated)
    _env_patch.start()

    loader = importlib.machinery.SourceFileLoader("omayt_under_test", str(OMAYT))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)


def tearDownModule() -> None:
    if _env_patch is not None:
        _env_patch.stop()
    if _isolated_home is not None:
        shutil.rmtree(_isolated_home, ignore_errors=True)


class KittyGraphicsDetection(unittest.TestCase):
    def detect(self, **env: str) -> bool:
        with mock.patch.dict(os.environ, env, clear=True):
            return module.terminal_supports_kitty_graphics()

    def test_kitty_window_id(self) -> None:
        self.assertTrue(self.detect(KITTY_WINDOW_ID="1", TERM="xterm-kitty"))

    def test_ghostty_resources_dir(self) -> None:
        self.assertTrue(self.detect(GHOSTTY_RESOURCES_DIR="/usr/share/ghostty"))

    def test_term_xterm_kitty(self) -> None:
        self.assertTrue(self.detect(TERM="xterm-kitty"))

    def test_term_program_herdr(self) -> None:
        self.assertTrue(self.detect(TERM="xterm-256color", TERM_PROGRAM="herdr"))

    def test_term_program_ghostty(self) -> None:
        self.assertTrue(self.detect(TERM="xterm-256color", TERM_PROGRAM="ghostty"))

    def test_term_program_wezterm_is_case_insensitive(self) -> None:
        self.assertTrue(self.detect(TERM="xterm-256color", TERM_PROGRAM="WezTerm"))

    def test_plain_xterm_is_not_kitty_graphics(self) -> None:
        self.assertFalse(
            self.detect(TERM="xterm-256color", TERM_PROGRAM="Apple_Terminal")
        )

    def test_empty_values_do_not_count(self) -> None:
        self.assertFalse(
            self.detect(
                KITTY_WINDOW_ID="",
                GHOSTTY_RESOURCES_DIR="",
                TERM="",
                TERM_PROGRAM="",
            )
        )

    def test_unknown_term_program_does_not_hide_xterm_kitty(self) -> None:
        self.assertTrue(self.detect(TERM="xterm-kitty", TERM_PROGRAM="tmux"))


class SingleDetectionPoint(unittest.TestCase):
    """The environment variables are read by the helper and nowhere else."""

    def setUp(self) -> None:
        self.source = OMAYT.read_text(encoding="utf-8")

    def test_kitty_window_id_is_read_once(self) -> None:
        self.assertEqual(self.source.count('os.environ.get("KITTY_WINDOW_ID")'), 1)

    def test_ghostty_resources_dir_is_read_once(self) -> None:
        self.assertEqual(self.source.count('os.environ.get("GHOSTTY_RESOURCES_DIR")'), 1)

    def test_term_is_read_once(self) -> None:
        self.assertEqual(self.source.count('os.environ.get("TERM"'), 1)

    def test_term_program_is_read_once(self) -> None:
        self.assertEqual(self.source.count('os.environ.get("TERM_PROGRAM"'), 1)

    def test_helper_is_used_by_every_consumer(self) -> None:
        # definition + thumbnail preview + both inline players + diagnostics
        self.assertGreaterEqual(self.source.count("terminal_supports_kitty_graphics()"), 5)


if __name__ == "__main__":
    unittest.main()
