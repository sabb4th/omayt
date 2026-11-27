"""A normal omayt start must not rewrite global mpv/yt-dlp configuration.

`~/.config/mpv/mpv.conf` and `~/.config/yt-dlp/config` are shared by every
other mpv and yt-dlp invocation on the machine, so omayt may only touch them
through an explicit request:

    omayt --fix-ytdlp          # command line
    [f] in Settings & Diagnostics

These tests run the real program (no imports, no mocking) with HOME, the XDG
dirs and a stub `fzf` on PATH redirected to a throw-away directory, so the
developer's own configuration and terminal are never read or written.

What actually guards the regression is the seeded case: a start must leave
already-existing shared files byte-identical. On the unfixed program the same
case fails, because start-up appended the "fix" lines to them.

Run with:

    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OMAYT = REPO_ROOT / "omayt"
TIMEOUT = 30
# How much of the child's stderr to attach to a failing assertion.
DIAGNOSTIC_TAIL = 2000


class IsolatedHomeTest(unittest.TestCase):
    """One temporary HOME per test, every XDG directory redirected into it."""

    def setUp(self) -> None:
        self.home = Path(tempfile.mkdtemp(prefix="omayt-test-"))
        self.addCleanup(shutil.rmtree, self.home, ignore_errors=True)
        self.config = self.home / ".config"
        (self.home / "tmp").mkdir(parents=True, exist_ok=True)
        # A stub fzf keeps the start path hermetic: run_tui() only needs the
        # binary to exist and to fail fast, which is exactly what it does
        # without a terminal. The suite no longer depends on the host's fzf.
        stub_bin = self.home / "bin"
        stub_bin.mkdir()
        fake_fzf = stub_bin / "fzf"
        fake_fzf.write_text("#!/bin/sh\nexit 2\n", encoding="utf-8")
        fake_fzf.chmod(0o755)

        self.env = dict(os.environ)
        self.env.update(
            {
                "HOME": str(self.home),
                "XDG_CONFIG_HOME": str(self.config),
                "XDG_CACHE_HOME": str(self.home / ".cache"),
                "XDG_DATA_HOME": str(self.home / ".local/share"),
                "XDG_STATE_HOME": str(self.home / ".local/state"),
                "TMPDIR": str(self.home / "tmp"),
                "OMAYT_LANG": "en",
                "PATH": f"{stub_bin}{os.pathsep}{os.environ.get('PATH', '')}",
            }
        )
        # The app must never see the real home while it runs.
        for name in ("MPV_HOME", "YTDLP_CONFIG", "OMARCHY_LANGUAGE_FILE"):
            self.env.pop(name, None)

    # -- paths under the isolated home -------------------------------------

    @property
    def mpv_conf(self) -> Path:
        return self.config / "mpv" / "mpv.conf"

    @property
    def ytdlp_conf(self) -> Path:
        return self.config / "yt-dlp" / "config"

    # -- helpers ----------------------------------------------------------

    def run_omayt(self, *args: str) -> subprocess.CompletedProcess[str]:
        """Run the real binary with no controlling terminal and no stdin.

        `start_new_session` detaches the child from the terminal, so the
        interactive menu cannot take over the screen: it falls back to the TUI
        and returns as soon as the stub fzf exits without output.
        """
        return subprocess.run(
            [sys.executable, str(OMAYT), *args],
            env=self.env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIMEOUT,
            start_new_session=True,
        )

    def assert_clean_exit(self, proc: subprocess.CompletedProcess[str]) -> None:
        """The start path must complete, not bail out on a missing dependency.

        `run_tui` returns 1 only when fzf is absent, so a zero exit status plus
        the fzf guard below keeps these cases on the code path that used to
        write the global configuration.
        """
        self.assertNotIn("Traceback", proc.stderr, proc.stderr[-DIAGNOSTIC_TAIL:])
        self.assertEqual(proc.returncode, 0, proc.stderr[-DIAGNOSTIC_TAIL:])

    def assert_no_global_config(self, proc: subprocess.CompletedProcess[str]) -> None:
        self.assert_clean_exit(proc)
        self.assertFalse(
            (self.config / "mpv").exists(),
            "a normal start created the global mpv config directory",
        )
        self.assertFalse(
            (self.config / "yt-dlp").exists(),
            "a normal start created the global yt-dlp config directory",
        )

    def seed_shared_config(self) -> dict[Path, bytes]:
        """Write the user's own shared config and return its exact bytes."""
        self.mpv_conf.parent.mkdir(parents=True, exist_ok=True)
        self.ytdlp_conf.parent.mkdir(parents=True, exist_ok=True)
        self.mpv_conf.write_text(
            "# my mpv config\nprofile=gpu-hq\n", encoding="utf-8"
        )
        self.ytdlp_conf.write_text("# my yt-dlp config\n--no-mtime\n", encoding="utf-8")
        return {
            path: path.read_bytes() for path in (self.mpv_conf, self.ytdlp_conf)
        }

    def assert_shared_config_unchanged(self, before: dict[Path, bytes]) -> None:
        for path, expected in before.items():
            self.assertEqual(
                path.read_bytes(),
                expected,
                f"a normal start modified {path}",
            )


class StartupDoesNotTouchGlobalConfig(IsolatedHomeTest):
    def test_help(self) -> None:
        proc = self.run_omayt("--help")
        self.assertEqual(proc.returncode, 0, proc.stderr[-DIAGNOSTIC_TAIL:])
        self.assertIn("omayt", proc.stdout)
        self.assert_no_global_config(proc)

    def test_bare_start(self) -> None:
        proc = self.run_omayt()
        self.assert_no_global_config(proc)

    def test_history_start(self) -> None:
        proc = self.run_omayt("-H")
        self.assert_no_global_config(proc)

    def test_version(self) -> None:
        proc = self.run_omayt("--version")
        self.assertEqual(proc.returncode, 0, proc.stderr[-DIAGNOSTIC_TAIL:])
        self.assert_no_global_config(proc)


class StartupLeavesExistingConfigAlone(IsolatedHomeTest):
    """The user already had these files; a start must not touch them."""

    def test_bare_start(self) -> None:
        before = self.seed_shared_config()
        self.assert_clean_exit(self.run_omayt())
        self.assert_shared_config_unchanged(before)

    def test_history_start(self) -> None:
        before = self.seed_shared_config()
        self.assert_clean_exit(self.run_omayt("-H"))
        self.assert_shared_config_unchanged(before)

    def test_help(self) -> None:
        before = self.seed_shared_config()
        self.assert_clean_exit(self.run_omayt("--help"))
        self.assert_shared_config_unchanged(before)


class ExplicitFixStillWrites(IsolatedHomeTest):
    def test_fix_ytdlp_writes_both_files(self) -> None:
        proc = self.run_omayt("--fix-ytdlp")
        self.assertEqual(proc.returncode, 0, proc.stderr[-DIAGNOSTIC_TAIL:])
        self.assertTrue(self.mpv_conf.is_file(), "mpv.conf was not written")
        self.assertTrue(self.ytdlp_conf.is_file(), "yt-dlp config was not written")
        self.assertIn("-tv_samsung", self.ytdlp_conf.read_text(encoding="utf-8"))
        # Only the key is asserted. A wrong backend value would still pass
        # here; that belongs to the change that picks the value.
        self.assertIn("hwdec=", self.mpv_conf.read_text(encoding="utf-8"))

    def test_fix_ytdlp_is_idempotent(self) -> None:
        self.run_omayt("--fix-ytdlp")
        self.run_omayt("--fix-ytdlp")
        ytdlp = self.ytdlp_conf.read_text(encoding="utf-8")
        mpv = self.mpv_conf.read_text(encoding="utf-8")
        self.assertEqual(ytdlp.count("-tv_samsung"), 1)
        self.assertEqual(mpv.count("hwdec="), 1)

    def test_fix_ytdlp_keeps_the_users_own_lines(self) -> None:
        self.mpv_conf.parent.mkdir(parents=True, exist_ok=True)
        self.mpv_conf.write_text("# my mpv config\nprofile=gpu-hq\n", encoding="utf-8")
        self.assert_clean_exit(self.run_omayt("--fix-ytdlp"))
        self.assertIn("profile=gpu-hq", self.mpv_conf.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
