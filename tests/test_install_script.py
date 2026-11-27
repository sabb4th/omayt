"""install.sh must not destroy a config the user already has.

Before this change it truncated `~/.config/ytfzf/conf.sh` and appended to
`~/.config/yt-dlp/config` with no backup. Both files belong to the user and may
be tuned already.

Each case runs the real script with HOME redirected to a temporary directory,
so the developer's own configuration is never touched.

Run with:

    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL = REPO_ROOT / "install.sh"
TIMEOUT = 60

YTFZF_SENTINEL = "# my own ytfzf config\nthumbnail_viewer=/usr/bin/chafa\n"
YTDLP_SENTINEL = "# my own yt-dlp config\n--no-mtime\n"
YTFZF_KEYS = ("show_thumbnails=1", "thumbnail_viewer=")


class InstallScriptTest(unittest.TestCase):
    def setUp(self) -> None:
        self.home = Path(tempfile.mkdtemp(prefix="omayt-install-"))
        self.addCleanup(shutil.rmtree, self.home, ignore_errors=True)
        self.ytfzf_conf = self.home / ".config/ytfzf/conf.sh"
        self.ytdlp_conf = self.home / ".config/yt-dlp/config"
        self.env = {
            "HOME": str(self.home),
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "TMPDIR": str(self.home),
        }

    def run_install(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(INSTALL)],
            env=self.env,
            cwd=str(REPO_ROOT),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIMEOUT,
        )

    def test_binary_is_installed_inside_the_isolated_home(self) -> None:
        proc = self.run_install()
        self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
        binary = self.home / ".local/bin/omayt"
        self.assertTrue(binary.is_file())
        self.assertTrue(os.access(binary, os.X_OK))

    def test_existing_ytfzf_conf_is_left_byte_identical(self) -> None:
        self.ytfzf_conf.parent.mkdir(parents=True)
        self.ytfzf_conf.write_text(YTFZF_SENTINEL, encoding="utf-8")
        before = self.ytfzf_conf.read_bytes()

        proc = self.run_install()
        self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
        self.assertEqual(self.ytfzf_conf.read_bytes(), before)
        self.assertIn("already exists", proc.stdout)

    def test_missing_ytfzf_conf_is_created(self) -> None:
        proc = self.run_install()
        self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])
        self.assertTrue(self.ytfzf_conf.is_file())
        body = self.ytfzf_conf.read_text(encoding="utf-8")
        for key in YTFZF_KEYS:
            self.assertIn(key, body)

    def test_existing_ytdlp_config_is_backed_up_before_appending(self) -> None:
        self.ytdlp_conf.parent.mkdir(parents=True)
        self.ytdlp_conf.write_text(YTDLP_SENTINEL, encoding="utf-8")

        proc = self.run_install()
        self.assertEqual(proc.returncode, 0, proc.stderr[-2000:])

        body = self.ytdlp_conf.read_text(encoding="utf-8")
        self.assertIn("--no-mtime", body)
        self.assertIn("-tv_samsung", body)

        backups = sorted(self.ytdlp_conf.parent.glob("config.bak.*"))
        self.assertEqual(len(backups), 1, backups)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), YTDLP_SENTINEL)

    def test_second_run_changes_nothing(self) -> None:
        self.assertEqual(self.run_install().returncode, 0)
        yt_dlp_first = self.ytdlp_conf.read_text(encoding="utf-8")
        ytfzf_first = self.ytfzf_conf.read_text(encoding="utf-8")

        self.assertEqual(self.run_install().returncode, 0)
        self.assertEqual(self.ytdlp_conf.read_text(encoding="utf-8"), yt_dlp_first)
        self.assertEqual(self.ytfzf_conf.read_text(encoding="utf-8"), ytfzf_first)
        self.assertEqual(self.ytdlp_conf.read_text(encoding="utf-8").count("-tv_samsung"), 1)
        self.assertEqual(len(list(self.ytdlp_conf.parent.glob("config.bak.*"))), 0)


if __name__ == "__main__":
    unittest.main()
