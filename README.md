<div align="center">

# omayt — Omarchy YouTube TUI

**A fast, visual terminal YouTube client with no API — built for the [Omarchy Linux](https://omarchy.org) ecosystem.**

[![Version](https://img.shields.io/badge/version-v1.3.0-89b4fa?style=for-the-badge)](https://github.com/sabb4th/omayt/releases)
[![Platform](https://img.shields.io/badge/platform-Omarchy%20%7C%20Arch%20Linux-a6e3a1?style=for-the-badge)](https://omarchy.org)
[![Python](https://img.shields.io/badge/python-Zero%20pip%20deps-94e2d5?style=for-the-badge)](./omayt)
[![Graphics](https://img.shields.io/badge/thumbnails-Sixel%20HD%20%C2%B7%20Kitty-f5c2e7?style=for-the-badge)](./omayt)
[![Audio](https://img.shields.io/badge/audio-Cava%20FFT%2060%20FPS-fab387?style=for-the-badge)](./omayt)
[![License](https://img.shields.io/badge/license-MIT-f9e2af?style=for-the-badge)](./LICENSE)

[Highlights](#-what-makes-it-good) • [Playback modes](#-4-playback-modes) • [Installation](#-dependencies--installation) • [CLI](#-how-to-use-cli) • [Shortcuts](#-shortcuts) • [Storage](#-local-storage)

<br />

<img src="assets/preview.png" alt="omayt v1.3.0 — Main menu on Omarchy Linux with the Catppuccin theme" width="100%" />

*Interactive main menu of `omayt v1.3.0` running in a floating window on Hyprland / Omarchy with the Catppuccin theme, synced automatically.*

</div>

---

## Why `omayt`?

**`omayt`** brings YouTube search, high-definition thumbnails, hardware acceleration and video and music playback together in **a single Python executable**, designed to work flawlessly on **Omarchy / Arch Linux** (terminals **Foot**, **Ghostty** and **Kitty**).

| Feature | How `omayt` solves it |
| :--- | :--- |
| **Zero API keys & zero Invidious** | Direct search through `yt-dlp`, with no dependency on YouTube Data API quotas or unstable Invidious instances. |
| **Zero `pip` dependencies** | Written entirely in the system's standard Python — no `venv`, no extra PyPI packages. |
| **Zero `HTTP 403` blocks** | 3-layer protection (*Anti-403*) with the `tv_samsung` profile bypass, `Ad-Wait Guard` and auto-reconnect. |
| **Zero AV1 stutter on the CPU** | Excludes AV1 streams (`[vcodec!^=av01]`) and prioritises **H.264 / VP9** with **VA-API** decoding on the GPU. |
| **Zero external `cava` needed** | A **Radix-2 FFT** spectrum visualiser at **60 FPS**, embedded directly in the audio player. |

---

## ✨ What makes it good

### 🎨 Hand-crafted main menu & native Omarchy theme sync
- **Flicker-free interface:** Alternate-screen rendering with synchronised updates (`\033[?2026h`), a pixel-art `OMAYT` logo with an animated TrueColor gradient, mini equalisers, a live status bar (active theme, `VA-API`, `Anti-403`, history counter) and your most recent searches.
- **Automatic Omarchy palette:** Reads `~/.local/state/omarchy/current/theme/colors.toml` and `theme.name` at startup and applies your theme's exact colours to the main menu, the `fzf` explorer, the preview pane and the Cava visualiser.
- **One-key navigation:** Press `1–7` to open any module directly, or `/` to start an immediate YouTube search.

### 🎵 Music mode with a built-in 60 FPS Cava spectrum visualiser
- **Real system audio capture:** Reads the output monitor at low latency (`18ms`) through **PipeWire** (`pw-record`) or **PulseAudio** (`parec` on `@DEFAULT_MONITOR@`).
- **Radix-2 FFT engine in pure Python:** 512 samples with a Hann window, dynamic AGC, gravity physics, a *Monstercat* filter and floating *Peak Caps*.
- **3 live visual styles (`v`):**
  1. **Cava Classic Bars** *(vertical bars with theme gradients and Peak Caps)*
  2. **Stereo Mirror (Monstercat)** *(L/R spectrum mirrored from the centre)*
  3. **Center Symmetrical** *(bass in the centre, treble at the edges)*
- **`mpv` IPC control:** Real-time progress bar, play/pause (`Space`), seek ±5s (`←/→`), volume (`↑/↓`) and mute (`m`) without leaving the terminal.

### 🖼️ HD thumbnails (Sixel & Kitty Graphics Protocol)
- **Parallel asynchronous prefetch:** Downloads thumbnails in the background (`ThreadPoolExecutor` with 10 workers) straight from the official CDN (`i.ytimg.com` — `maxresdefault.jpg`, falling back to `sddefault` and `hqdefault`).
- **Exact pixel sizing:** Queries `TIOCGWINSZ` to compute the ideal thumbnail width up to `1152px` (`1280px` in direct Sixel mode) with an exact 16:9 ratio.
- **Definitive fix for Arch Linux (`gdk-pixbuf2` / `glycin`):** On recent Arch, the `/usr/bin/img2sixel` utility can fail and return `0 bytes`. `omayt` works around it by decoding the image with `ffmpeg` (16:9 crop + **Lanczos** scaling + `unsharp` sharpening) and calling `sixel_encoder_encode_bytes` in memory directly against `libsixel.so.1` through `ctypes`, with a `.sixel` cache on disk.
- **Multi-terminal:** Uses `kitten icat` (`--transfer-mode=memory --unicode-placeholder`) on **Kitty** and **Ghostty**, native HD Sixel on **Foot**, and falls back to `chafa` automatically.

### ⚡ VA-API hardware acceleration & AV1 exclusion
- Prioritises **H.264 / VP9** streams (`[vcodec!^=av01]`) up to **1080p** in the `mpv` window (`--hwdec=vaapi,vaapi-copy`) and up to **720p** in the terminal's inline modes (`--hwdec=vaapi-copy`).
- Avoids heavy software AV1 decoding and works around common Vulkan Video (`VK_KHR_video_decode_queue`) failures on Intel Iris Xe, AMD and Mesa GPUs.

### 🛡️ Triple Anti-403 protection (`tv_samsung` bypass + `Ad-Wait Guard`)
1. **`tv_samsung` client bypass:** Injects `--extractor-args "youtube:player_client=default,-tv_samsung"` into `yt-dlp` and `mpv` (`--ytdl-raw-options-append`).
2. **`Ad-Wait Guard` interceptor in `mpv`'s `ytdl_hook`:** `omayt` acts as a `yt-dlp` wrapper, inspects the `available_at` field of the returned stream JSON and waits for the exact release moment with a visual countdown in the terminal before handing the URL to `ffmpeg`.
3. **HTTP 4xx auto-reconnect:** Sets `--stream-lavf-o=reconnect=1,reconnect_streamed=1,reconnect_on_http_error=4xx,reconnect_delay_max=5` and retries automatically if the stream is withheld in the first seconds.

<details>
<summary><strong>Why does the HTTP 403 Forbidden error happen in traditional clients?</strong></summary>

Traditional terminal clients (`ytfzf` or plain `mpv`) often fail with `HTTP 403 Forbidden` because `yt-dlp` uses the `tv_samsung` (Smart TV) profile by default, on which YouTube applies a wait window of ~3 to 5 seconds (`available_at`) simulating the time to "skip an ad". While `yt-dlp` in download mode waits out that interval, `mpv` extracts the JSON through `yt-dlp -J` and tries to open the URL immediately in `ffmpeg`, receiving `403 Forbidden`. The 3 layers of `omayt` eliminate that problem at the root.

</details>

### 🔎 Channel search (`channel/`), search filters (`Alt+F`), paginated search & diagnostics
- **Channel-only search (`channel/`):** Type `name/` (e.g. `raimundo/`) to list **only videos from that channel** (newest first, with +30 pagination), or `name/topic` (e.g. `raimundo/bitcoin`) to search within that channel.
- **Search filters (`Alt+F`):** Press `Alt+F` (or `Ctrl+O`) inside the TUI — or `Tab` / `Alt+F` in the search modal — to filter results by **Today**, **This week**, **This month**, **This year**, **Most viewed**, **Short (< 3 min)**, **Medium (3–20 min)**, **Long (> 20 min)** or **Live**.
- **30-at-a-time pagination:** Every search loads 30 results and lets you expand **+30 results** on demand (`Alt+M`, `Ctrl+E` or by selecting the item at the end of the list), preserving order and cursor position.
- **Direct link / URL (`[5]`):** Accepts full URLs (`youtube.com/watch`, `youtu.be`, `shorts`, `live`, `embed`) or 11-character IDs, with **clipboard auto-detection** through `wl-paste` and a choice of player (*MPV window*, *Sixel/Kitty terminal*, *Cava* or *Download*).
- **Downloads & offline library (`Alt+D` / `[6]`):** Download videos as **MP4 (1080p H.264/VP9)** or audio only as **MP3** into `~/Videos/omayt/`, and play the local files straight from the menu.
- **Settings & diagnostics (`[7]`):** Checks every system dependency, shows swatches of the active Omarchy palette, displays HD cache/history statistics and lets you apply optimisations (`f`) or clear cache/searches (`c` / `h`) in one keystroke.
- **Automatic `ytfzf` migration:** Imports your existing history from `~/.cache/ytfzf/watch_hist` on the first run if `omayt`'s history is still empty.

---

## 🎬 4 playback modes

| Mode | TUI shortcut | Engine / protocol | Quality & HWDec | Best for |
| :--- | :--- | :--- | :--- | :--- |
| **MPV window** | `Enter` *(or `Alt+W`)* | Native `mpv` (Wayland) | Up to **1080p** · `vaapi,vaapi-copy` | Watching fullscreen or in a floating window with GPU acceleration |
| **Inline video in pixels** | `Alt+I` *(or `Ctrl+T`)* | `mpv --vo=sixel` *(Foot)* / `--vo=kitty` *(Kitty/Ghostty)* | Up to **720p** · `vaapi-copy` | Watching inside the terminal window itself, in real pixels |
| **TrueColor blocks** | `Alt+B` | `mpv --vo=tct` | Up to **720p** · `vaapi-copy` | Universal compatibility with any TrueColor terminal |
| **Music mode + Cava** | `Alt+A` *(or `[4]` in the menu)* | `mpv --no-video` + IPC + 60 FPS FFT | `bestaudio/best` | Listening to music and podcasts with a live spectrum visualiser |

---

## 📦 Dependencies & installation

### Dependencies on Omarchy / Arch Linux

- **Required:** `python` (the system's Python 3), `fzf` (`>= 0.50`), `yt-dlp`, `mpv`, `ffmpeg`, `libsixel`
- **Optional (recommended):** `wl-clipboard` (copy/paste links on Wayland), `libnotify` (notifications when copying a link), `chafa` (graphics fallback) and PipeWire/PulseAudio (`pw-record` or `parec`) for the Cava visualiser.

```bash
omarchy pkg add fzf yt-dlp mpv ffmpeg libsixel
```

### Option 1: Installer script (`install.sh`)

```bash
git clone https://github.com/sabb4th/omayt.git
cd omayt
chmod +x install.sh omayt
./install.sh
```

`install.sh` performs 3 steps automatically:
1. Installs the executable at `~/.local/bin/omayt`;
2. Configures `~/.config/yt-dlp/config` with `--extractor-args "youtube:player_client=default,-tv_samsung"`;
3. Configures `~/.config/ytfzf/conf.sh` and `~/.config/ytfzf/thumbnail-viewers/sixel-inline` to use `omayt`'s Sixel renderer (`omayt --sixel`).

### Option 2: Arch Linux package (`PKGBUILD`)

```bash
makepkg -si
```

---

## 🚀 How to use (CLI)

```bash
# Open the interactive main menu
omayt

# Search YouTube directly (30 initial results + HD thumbnails)
omayt "omarchy linux"

# List all videos from a specific channel (or search inside that channel)
omayt "raimundo/"
omayt "raimundo/bitcoin"

# Search with a filter directly from CLI (today, week, month, year, views, short, medium, long, live)
omayt --filter views "omarchy linux"

# Skip the splash menu and open the TUI explorer (fzf) directly
omayt --no-menu
omayt -t

# Open the watched-videos history directly
omayt -H
omayt --history

# Apply the global Anti-403, no-AV1 and VA-API optimisations to yt-dlp and mpv
omayt --fix-ytdlp

# Render any image as HD Sixel in the Foot terminal
omayt --sixel path/to/image.jpg 640

# Show version or help
omayt -v
omayt -h
```

### 🌍 Interface language

The interface ships in **English**, **Brazilian Portuguese** and **French** — main menu, `fzf` labels, preview pane, player banners and `--help`. On first launch it automatically follows your **Omarchy language** (`~/.config/omarchy/language`) and can be switched anytime in **[7] Settings & Diagnostics** (`[e]` English, `[p]` Portuguese (Brazil), `[r]` French, `[l]` toggle) or per-run via `--lang en|fr|pt`. Resolution order:

1. `--lang en|fr|pt` (CLI flag) or `OMAYT_LANG` (`en`, `pt`, `fr`, plus `pt_BR`, `pt-PT`, `fr_FR`, `fr-CA`…);
2. the language saved in **[7] Settings & Diagnostics** (`~/.config/omayt/settings.json`);
3. **Omarchy's system language** (`~/.config/omarchy/language`, e.g. `pt-BR` starts in Portuguese, `en` starts in English);
4. your system locale (`LC_ALL` / `LC_MESSAGES` / `LANG`);
5. English otherwise.

```bash
# One run only, without touching the saved preference
omayt --lang en
OMAYT_LANG=pt omayt
```

---

## ⌨️ Shortcuts

### Main menu

| Key | Action |
| :--- | :--- |
| **`↑` / `↓`** or **`j` / `k`** | Move between the options |
| **`Enter`** | Open the selected item |
| **`/`** | Open a quick YouTube search |
| **`1` – `7`** | Direct access to the menu modules |
| **`0` / `q` / `Esc`** | Quit `omayt` |

### TUI explorer (`fzf`)

| Shortcut | Action |
| :--- | :--- |
| **`Enter`** | Watch in **`mpv`** *(or play in Cava in music mode; searches on the first line ` ` / loads +30 on the last line `󰐕`)* |
| **`Ctrl+S`** | **Search YouTube** for the term typed in the top bar *(30 results; supports `channel/` and `channel/topic`)* |
| **`Alt+F`** *(or `Ctrl+O`)* | **Choose search filter** *(Relevance, Today, Week, Month, Year, Most viewed, Short, Medium, Long, Live)* |
| **`Alt+M`** *(or `Ctrl+E`)* | **Load +30 results** for the current search *(30-at-a-time pagination)* |
| **`Alt+I`** *(or `Ctrl+T`)* | Watch **inside the terminal** in real pixels (`--vo=sixel` / `--vo=kitty`) |
| **`Alt+B`** | Watch inside the terminal in **TrueColor blocks** (`--vo=tct`) |
| **`Alt+A`** | Play **audio only** with the **60 FPS Cava spectrum visualiser** |
| **`Alt+W`** | Force opening in the **MPV window** *(useful when in music mode)* |
| **`Alt+D`** | Download the **video (MP4)** or the **audio (MP3)** into `~/Videos/omayt` |
| **`Alt+L`** | Copy the video link to the clipboard (`wl-copy`) |
| **`Ctrl+H`** | Open the **History** of watched videos |
| **`Ctrl+F`** | Toggle a local filter on the current list |
| **`Esc` / `Ctrl+C`** | Back to the main menu *(or quit)* |

### Music player (Cava visualiser)

| Key | Action |
| :--- | :--- |
| **`Space`** | Play / Pause |
| **`←` / `→`** | Seek forward / backward 5 seconds |
| **`↑` / `↓`** | Increase / decrease volume |
| **`m`** | Mute / unmute |
| **`v`** | Cycle the visualiser style *(Classic Bars / Stereo Mirror / Center Symmetrical)* |
| **`q` / `Esc`** | Back to the TUI |

---

## 🗂️ Local storage

`omayt` does not download videos to disk when streaming; only metadata, history and cached thumbnails are stored locally:

- **`~/.cache/omayt/thumbs_hd/`**: Cache of `.jpg` thumbnails and pre-encoded `.sixel` versions.
- **`~/.cache/omayt/videos_db.json`**, **`last_list.json`**, **`state.json`**: Video metadata and the state of the last session/search.
- **`~/.config/omayt/watch_history.json`**: Local history of watched videos (`Ctrl+H`).
- **`~/.config/omayt/search_history.json`**: History of recent searches shown in the main menu.
- **`~/Videos/omayt/`**: MP4/MP3 download folder (created only when downloading with `Alt+D`).

You can manage and clear cache or history from the **`[7] Settings & diagnostics`** menu, or manually with:

```bash
rm -rf ~/.cache/omayt ~/.config/omayt
```

---

## 📄 License

Distributed under the [MIT](./LICENSE) license.
