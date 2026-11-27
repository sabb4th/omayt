"""Remote titles and channel names must never reach the terminal as escapes.

A video title is attacker-controlled text that omayt prints with ANSI colours
enabled, so an OSC or CSI sequence in it would be interpreted by the terminal
(clipboard writes, palette changes). The render path strips them first.

Run with:

    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import os
import shutil
import subprocess
import sys
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
    global module, _isolated_home, _env_patch
    _isolated_home = Path(tempfile.mkdtemp(prefix="omayt-escapes-"))
    _env_patch = mock.patch.dict(
        os.environ,
        {
            "HOME": str(_isolated_home),
            "XDG_CONFIG_HOME": str(_isolated_home / ".config"),
            "XDG_CACHE_HOME": str(_isolated_home / ".cache"),
            "XDG_DATA_HOME": str(_isolated_home / ".local/share"),
            "XDG_STATE_HOME": str(_isolated_home / ".local/state"),
            "OMAYT_LANG": "en",
        },
    )
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


class StripHelper(unittest.TestCase):
    def strip(self, text: object) -> str:
        return module.strip_terminal_escapes(text)

    def test_osc_clipboard_payload_is_removed(self) -> None:
        self.assertEqual(self.strip("clash royale \x1b]52;c;AAAA\x07"), "clash royale ")

    def test_csi_colour_is_removed(self) -> None:
        self.assertEqual(self.strip("\x1b[31mred\x1b[0m"), "red")

    def test_st_terminated_osc_is_removed(self) -> None:
        self.assertEqual(self.strip("\x1b]0;title\x1b\\done"), "done")

    def test_control_characters_are_removed(self) -> None:
        self.assertEqual(self.strip("a\tb\nc\x07d\x7fe\x9bf"), "abcdef")

    def test_visible_unicode_survives(self) -> None:
        text = "日本語 🎬 ünïcode \uf0c1"
        self.assertEqual(self.strip(text), text)

    def test_empty_and_none(self) -> None:
        self.assertEqual(self.strip(""), "")
        self.assertEqual(self.strip(None), "")

    def test_idempotent(self) -> None:
        once = self.strip("\x1b[1mhello\x1b[0m")
        self.assertEqual(self.strip(once), once)


class RenderPathRemovesEscapes(unittest.TestCase):
    """The real program, printing a cached title that carries escapes."""

    def test_internal_rows_have_no_escape_sequences(self) -> None:
        home = Path(tempfile.mkdtemp(prefix="omayt-escapes-run-"))
        self.addCleanup(shutil.rmtree, home, ignore_errors=True)
        cache = home / ".cache" / "omayt"
        cache.mkdir(parents=True)

        hostile = "clash royale \x1b]52;c;Q0xJUEJPQVJE\x07\x1b[31mred\x1b[0m"
        (cache / "last_list.json").write_text(
            json.dumps(
                [
                    {
                        "id": "dQw4w9WgXcQ",
                        "title": hostile,
                        "channel": "\x1b[35mchan\x1b[0m",
                        "duration": "03:32",
                        "views": "1.0M",
                        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    }
                ]
            ),
            encoding="utf-8",
        )

        env = dict(os.environ)
        env.update(
            {
                "HOME": str(home),
                "XDG_CONFIG_HOME": str(home / ".config"),
                "XDG_CACHE_HOME": str(home / ".cache"),
                "XDG_STATE_HOME": str(home / ".local/state"),
                "TMPDIR": str(home),
                "OMAYT_LANG": "en",
            }
        )
        proc = subprocess.run(
            [sys.executable, str(OMAYT), "--internal-search"],
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
        self.assertIn("clash royale", proc.stdout)
        self.assertNotIn("]52", proc.stdout)
        self.assertNotIn("\x07", proc.stdout)
        self.assertNotIn("\x1b[31m", proc.stdout)
        self.assertNotIn("\x1b[35m", proc.stdout)


if __name__ == "__main__":
    unittest.main()
