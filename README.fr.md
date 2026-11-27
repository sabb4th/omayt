<div align="center">

# 󰗃 omayt — Omarchy YouTube TUI

**Un client YouTube de terminal rapide et visuel, sans API — conçu pour l'écosystème [Omarchy Linux](https://omarchy.org).**

[![Version](https://img.shields.io/badge/version-v1.4.0-89b4fa?style=for-the-badge)](https://github.com/sabb4th/omayt/releases)
[![Platform](https://img.shields.io/badge/platform-Omarchy%20%7C%20Arch%20Linux-a6e3a1?style=for-the-badge)](https://omarchy.org)
[![Python](https://img.shields.io/badge/python-Zero%20pip%20deps-94e2d5?style=for-the-badge)](./omayt)
[![Graphics](https://img.shields.io/badge/thumbnails-Sixel%20HD%20%C2%B7%20Kitty-f5c2e7?style=for-the-badge)](./omayt)
[![Audio](https://img.shields.io/badge/audio-Cava%20FFT%2060%20FPS-fab387?style=for-the-badge)](./omayt)
[![License](https://img.shields.io/badge/license-MIT-f9e2af?style=for-the-badge)](./LICENSE)

[Points forts](#-ce-qui-le-rend-bon) • [Captures](#️-captures-décran) • [Nouveautés](#-nouveautés-de-la-v140) • [Modes de lecture](#-4-modes-de-lecture) • [Installation](#-dépendances--installation) • [CLI](#-utilisation-cli) • [Raccourcis](#️-raccourcis) • [Stockage](#️-stockage-local)

<br />

<img src="assets/preview.png" alt="omayt v1.4.0 — Menu principal sur Omarchy Linux avec le thème Catppuccin" width="100%" />

*Menu principal interactif d'`omayt v1.4.0` exécuté dans une fenêtre flottante sur Hyprland / Omarchy avec le thème Catppuccin, synchronisé automatiquement.*

</div>

---

## Pourquoi `omayt` ?

**`omayt`** réunit la recherche YouTube, les vignettes haute définition, l'accélération matérielle et la lecture de vidéos et de musique dans **un seul exécutable Python**, conçu pour fonctionner parfaitement sur **Omarchy / Arch Linux** (terminaux **Foot**, **Ghostty** et **Kitty**).

| Fonctionnalité | Comment `omayt` y répond |
| :--- | :--- |
| **Zéro clé API & zéro Invidious** | Recherche directe via `yt-dlp`, sans dépendre des quotas de l'API YouTube Data ni d'instances Invidious instables. |
| **Zéro dépendance `pip`** | Écrit entièrement avec le Python standard du système — pas de `venv`, aucun paquet PyPI supplémentaire. |
| **Zéro blocage `HTTP 403`** | Protection en 3 couches (*Anti-403*) avec le contournement du profil `tv_samsung`, `Ad-Wait Guard` et reconnexion automatique. |
| **Zéro saccade AV1 sur le CPU** | Exclut les flux AV1 (`[vcodec!^=av01]`) et privilégie **H.264 / VP9** avec décodage **VA-API** sur le GPU. |
| **Zéro `cava` externe nécessaire** | Un visualiseur de spectre **FFT Radix-2** à **60 FPS**, intégré directement au lecteur audio. |

---

## 🚀 Démarrage rapide

```bash
git clone https://github.com/sabb4th/omayt.git && cd omayt && ./install.sh
omayt                      # menu interactif
omayt "omarchy linux"      # recherche directe
omayt "raimundo/"          # toutes les vidéos d'une chaîne
omayt --lang en            # force la langue de l'interface (en / pt / fr)
```

## 🖼️ Captures d'écran

`omayt` lit le **thème Omarchy actif** au démarrage : le menu suit le thème que vous choisissez, sans aucune configuration.

| | |
| :---: | :---: |
| <img src="assets/preview.png" alt="Catppuccin" width="100%" /><br/>**Catppuccin** | <img src="assets/screenshot-catppuccin-latte.png" alt="Catppuccin Latte" width="100%" /><br/>**Catppuccin Latte** |
| <img src="assets/screenshot-earth.png" alt="Earth" width="100%" /><br/>**Earth** | <img src="assets/screenshot-jade-horse.png" alt="Jade Horse" width="100%" /><br/>**Jade Horse** |
| <img src="assets/screenshot-gruvbox.png" alt="Gruvbox" width="100%" /><br/>**Gruvbox** | |

> Les captures ont été réalisées avec la `v1.3.0` et l'interface en portugais ; depuis la `v1.4.0`, toute l'interface suit la langue choisie (English, Português ou Français).

## 🆕 Nouveautés de la v1.4.0

- **Interface entièrement en anglais :** libellés, modales, aperçus, bandeaux des lecteurs et `--help` suivent la langue choisie — y compris les vidéos en cache (`AO VIVO` → `LIVE`, `Sem título` → `Untitled`).
- **Langue partout :** détection de la langue d'Omarchy, `--lang en|fr|pt`, `OMAYT_LANG` et `[e]` / `[p]` / `[r]` / `[l]` dans les Paramètres, propagée à `fzf`, `mpv` et `yt-dlp`.
- **Recherche par chaîne :** `nom/` liste les vidéos d'une chaîne, `nom/sujet` cherche dedans, avec pagination +30.
- **Filtres de recherche :** `Alt+F` (ou `--filter`) — Aujourd'hui, Cette semaine, Ce mois-ci, Cette année, Les plus vues, Courtes, Moyennes, Longues, En direct.

---

## ✨ Ce qui le rend bon

### 🎨 Menu principal fait main & synchronisation native du thème Omarchy
- **Interface sans scintillement :** rendu en écran alterné avec mises à jour synchronisées (`\033[?2026h`), logo `OMAYT` en pixel art avec dégradé TrueColor animé, mini-égaliseurs, barre d'état en direct (thème actif, `VA-API`, `Anti-403`, compteur d'historique) et vos recherches les plus récentes.
- **Palette Omarchy automatique :** lit `~/.local/state/omarchy/current/theme/colors.toml` et `theme.name` au démarrage et applique les couleurs exactes de votre thème au menu principal, à l'explorateur `fzf`, au volet d'aperçu et au visualiseur Cava.
- **Navigation à une touche :** appuyez sur `1–7` pour ouvrir n'importe quel module directement, ou sur `/` pour lancer immédiatement une recherche YouTube.

### 🎵 Mode musique avec visualiseur de spectre Cava 60 FPS intégré
- **Capture réelle de l'audio système :** lit le moniteur de sortie à faible latence (`18ms`) via **PipeWire** (`pw-record`) ou **PulseAudio** (`parec` sur `@DEFAULT_MONITOR@`).
- **Moteur FFT Radix-2 en Python pur :** 512 échantillons avec fenêtre de Hann, AGC dynamique, physique de gravité, filtre *Monstercat* et *Peak Caps* flottants.
- **3 styles visuels en direct (`v`) :**
  1. **Cava Classic Bars** *(barres verticales avec dégradés du thème et Peak Caps)*
  2. **Stereo Mirror (Monstercat)** *(spectre G/D mis en miroir depuis le centre)*
  3. **Center Symmetrical** *(basses au centre, aigus sur les bords)*
- **Contrôle IPC de `mpv` :** barre de progression en temps réel, lecture/pause (`Space`), déplacement de ±5s (`←/→`), volume (`↑/↓`) et muet (`m`) sans quitter le terminal.

### 🖼️ Vignettes HD (Sixel & Kitty Graphics Protocol)
- **Préchargement asynchrone parallèle :** télécharge les vignettes en arrière-plan (`ThreadPoolExecutor` avec 10 workers) directement depuis le CDN officiel (`i.ytimg.com` — `maxresdefault.jpg`, avec repli sur `sddefault` et `hqdefault`).
- **Dimensionnement exact en pixels :** interroge `TIOCGWINSZ` pour calculer la largeur idéale de la vignette jusqu'à `1152px` (`1280px` en mode Sixel direct) avec un ratio 16:9 exact.
- **Correctif définitif pour Arch Linux (`gdk-pixbuf2` / `glycin`) :** sur un Arch récent, l'utilitaire `/usr/bin/img2sixel` peut échouer et renvoyer `0 bytes`. `omayt` le contourne en décodant l'image avec `ffmpeg` (recadrage 16:9 + mise à l'échelle **Lanczos** + accentuation `unsharp`) et en appelant `sixel_encoder_encode_bytes` en mémoire directement sur `libsixel.so.1` via `ctypes`, avec un cache `.sixel` sur disque.
- **Multi-terminal :** utilise `kitten icat` (`--transfer-mode=memory --unicode-placeholder`) sur **Kitty** et **Ghostty**, le Sixel HD natif sur **Foot**, et retombe automatiquement sur `chafa`.

### ⚡ Accélération matérielle VA-API & exclusion de l'AV1
- Privilégie les flux **H.264 / VP9** (`[vcodec!^=av01]`) jusqu'à **1080p** dans la fenêtre `mpv` (`--hwdec=vaapi,vaapi-copy`) et jusqu'à **720p** dans les modes intégrés au terminal (`--hwdec=vaapi-copy`).
- Évite le décodage logiciel AV1, coûteux, et contourne les défaillances courantes de Vulkan Video (`VK_KHR_video_decode_queue`) sur les GPU Intel Iris Xe, AMD et Mesa.

### 🛡️ Triple protection Anti-403 (contournement `tv_samsung` + `Ad-Wait Guard`)
1. **Contournement du client `tv_samsung` :** injecte `--extractor-args "youtube:player_client=default,-tv_samsung"` dans `yt-dlp` et `mpv` (`--ytdl-raw-options-append`).
2. **Intercepteur `Ad-Wait Guard` dans le `ytdl_hook` de `mpv` :** `omayt` se comporte comme un wrapper de `yt-dlp`, inspecte le champ `available_at` du JSON de flux renvoyé et attend l'instant exact de la mise à disposition avec un compte à rebours visuel dans le terminal, avant de transmettre l'URL à `ffmpeg`.
3. **Reconnexion automatique sur HTTP 4xx :** définit `--stream-lavf-o=reconnect=1,reconnect_streamed=1,reconnect_on_http_error=4xx,reconnect_delay_max=5` et réessaie automatiquement si le flux est retenu dans les premières secondes.

<details>
<summary><strong>Pourquoi l'erreur HTTP 403 Forbidden survient-elle dans les clients traditionnels ?</strong></summary>

Les clients de terminal traditionnels (`ytfzf` ou `mpv` seul) échouent souvent avec `HTTP 403 Forbidden` parce que `yt-dlp` utilise par défaut le profil `tv_samsung` (Smart TV), sur lequel YouTube applique une fenêtre d'attente d'environ 3 à 5 secondes (`available_at`) simulant le temps nécessaire pour « passer une publicité ». Alors que `yt-dlp` en mode téléchargement attend cet intervalle, `mpv` extrait le JSON via `yt-dlp -J` et tente d'ouvrir l'URL immédiatement dans `ffmpeg`, en recevant `403 Forbidden`. Les 3 couches d'`omayt` éliminent ce problème à la racine.

</details>

### 🔎 Recherche par chaîne (`chaîne/`), filtres de recherche (`Alt+F`), pagination & diagnostics
- **Recherche dédiée à une chaîne (`chaîne/`) :** saisissez `nom/` (ex. `raimundo/`) pour lister **uniquement les vidéos de cette chaîne** (du plus récent au plus ancien, avec pagination +30), ou `nom/sujet` (ex. `raimundo/bitcoin`) pour rechercher dans cette chaîne.
- **Filtres de recherche (`Alt+F`) :** appuyez sur `Alt+F` (ou `Ctrl+O`) dans la TUI — ou `Tab` / `Alt+F` dans la fenêtre de recherche — pour filtrer par **Aujourd'hui**, **Cette semaine**, **Ce mois-ci**, **Cette année**, **Les plus vues**, **Courtes (< 3 min)**, **Moyennes (3–20 min)**, **Longues (> 20 min)** ou **En direct**.
- **Pagination par 30 :** chaque recherche charge 30 résultats et permet d'en étendre **+30** à la demande (`Alt+M`, `Ctrl+E` ou en sélectionnant l'élément en fin de liste), en préservant l'ordre et la position du curseur.
- **Lien direct / URL (`[5]`) :** accepte les URL complètes (`youtube.com/watch`, `youtu.be`, `shorts`, `live`, `embed`) ou les ID de 11 caractères, avec **détection automatique du presse-papiers** via `wl-paste` et un choix du lecteur (*Fenêtre MPV*, *Terminal Sixel/Kitty*, *Cava* ou *Téléchargement*).
- **Téléchargements & bibliothèque hors ligne (`Alt+D` / `[6]`) :** télécharge les vidéos en **MP4 (1080p H.264/VP9)** ou l'audio seul en **MP3** dans `~/Videos/omayt/`, et lit les fichiers locaux directement depuis le menu.
- **Paramètres & diagnostics (`[7]`) :** vérifie chaque dépendance système, affiche des échantillons de la palette Omarchy active, présente les statistiques du cache HD et de l'historique et permet d'appliquer des optimisations (`f`) ou de vider cache/recherches (`c` / `h`) en une seule touche.
- **Migration automatique depuis `ytfzf` :** importe votre historique existant depuis `~/.cache/ytfzf/watch_hist` au premier lancement si l'historique d'`omayt` est encore vide.

---

## 🎬 4 modes de lecture

| Mode | Raccourci TUI | Moteur / protocole | Qualité & HWDec | Idéal pour |
| :--- | :--- | :--- | :--- | :--- |
| **Fenêtre MPV** | `Enter` *(ou `Alt+W`)* | `mpv` natif (Wayland) | Jusqu'à **1080p** · `vaapi,vaapi-copy` | Regarder en plein écran ou dans une fenêtre flottante avec accélération GPU |
| **Vidéo intégrée en pixels** | `Alt+I` *(ou `Ctrl+T`)* | `mpv --vo=sixel` *(Foot)* / `--vo=kitty` *(Kitty/Ghostty)* | Jusqu'à **720p** · `vaapi-copy` | Regarder à l'intérieur même de la fenêtre du terminal, en vrais pixels |
| **Blocs TrueColor** | `Alt+B` | `mpv --vo=tct` | Jusqu'à **720p** · `vaapi-copy` | Compatibilité universelle avec n'importe quel terminal TrueColor |
| **Mode musique + Cava** | `Alt+A` *(ou `[4]` dans le menu)* | `mpv --no-video` + IPC + FFT 60 FPS | `bestaudio/best` | Écouter de la musique et des podcasts avec un visualiseur de spectre en direct |

---

## 📦 Dépendances & installation

### Dépendances sous Omarchy / Arch Linux

- **Requis :** `python` (le Python 3 du système), `fzf` (`>= 0.50`), `yt-dlp`, `mpv`, `ffmpeg`, `libsixel`
- **Facultatif (recommandé) :** `wl-clipboard` (copier/coller des liens sous Wayland), `libnotify` (notifications lors de la copie d'un lien), `chafa` (repli graphique) et PipeWire/PulseAudio (`pw-record` ou `parec`) pour le visualiseur Cava.

```bash
omarchy pkg add fzf yt-dlp mpv ffmpeg libsixel
```

### Option 1 : script d'installation (`install.sh`)

```bash
git clone https://github.com/sabb4th/omayt.git
cd omayt
chmod +x install.sh omayt
./install.sh
```

`install.sh` effectue 3 étapes automatiquement :
1. Installe l'exécutable dans `~/.local/bin/omayt` ;
2. Configure `~/.config/yt-dlp/config` avec `--extractor-args "youtube:player_client=default,-tv_samsung"` ;
3. Configure `~/.config/ytfzf/conf.sh` et `~/.config/ytfzf/thumbnail-viewers/sixel-inline` pour utiliser le moteur de rendu Sixel d'`omayt` (`omayt --sixel`).

### Option 2 : paquet Arch Linux (`PKGBUILD`)

```bash
makepkg -si
```

---

## 🚀 Utilisation (CLI)

```bash
# Ouvre le menu principal interactif
omayt

# Recherche directement sur YouTube (30 résultats initiaux + vignettes HD)
omayt "omarchy linux"

# Liste toutes les vidéos d'une chaîne précise (ou recherche dans cette chaîne)
omayt "raimundo/"
omayt "raimundo/bitcoin"

# Recherche avec un filtre depuis la CLI (today, week, month, year, views, short, medium, long, live)
omayt --filter views "omarchy linux"

# Ignore le menu d'accueil et ouvre directement l'explorateur TUI (fzf)
omayt --no-menu
omayt -t

# Ouvre directement l'historique des vidéos regardées
omayt -H
omayt --history

# Applique les optimisations globales Anti-403, sans AV1 et VA-API à yt-dlp et mpv
omayt --fix-ytdlp

# Affiche n'importe quelle image en Sixel HD dans le terminal Foot
omayt --sixel path/to/image.jpg 640

# Affiche la version ou l'aide
omayt -v
omayt -h
```

### 🌍 Langue de l'interface

L'interface est livrée en **anglais**, en **portugais du Brésil** et en **français** — menu principal, libellés `fzf`, volet d'aperçu, bandeaux des lecteurs et `--help`. Au premier lancement, elle suit automatiquement la **langue d'Omarchy** (`~/.config/omarchy/language`) et peut être modifiée à tout moment dans **[7] Paramètres & diagnostics** (`[e]` English, `[p]` Portugais (Brésil), `[r]` Français, `[l]` basculer) ou ponctuellement via `--lang en|fr|pt`. Ordre de priorité :

1. `--lang en|fr|pt` (option CLI) ou `OMAYT_LANG` (`en`, `pt`, `fr`, ainsi que `pt_BR`, `pt-PT`, `fr_FR`, `fr-CA`…), toujours prioritaire ;
2. la langue enregistrée dans **[7] Paramètres & diagnostics** (`~/.config/omayt/settings.json`) ;
3. la **langue système d'Omarchy** (`~/.config/omarchy/language`) ;
4. votre locale système (`LC_ALL` / `LC_MESSAGES` / `LANG`) ;
5. l'anglais sinon.

```bash
# Pour un seul lancement, sans toucher au réglage enregistré
omayt --lang en
OMAYT_LANG=pt omayt
```

---

## ⌨️ Raccourcis

### Menu principal

| Touche | Action |
| :--- | :--- |
| **`↑` / `↓`** ou **`j` / `k`** | Se déplacer entre les options |
| **`Enter`** | Ouvrir l'élément sélectionné |
| **`/`** | Ouvrir une recherche YouTube rapide |
| **`1` – `7`** | Accès direct aux modules du menu |
| **`0` / `q` / `Esc`** | Quitter `omayt` |

### Explorateur TUI (`fzf`)

| Raccourci | Action |
| :--- | :--- |
| **`Enter`** | Regarder dans **`mpv`** *(ou lire dans Cava en mode musique ; rechercher sur la première ligne ` ` / charger +30 sur la dernière ligne `󰐕`)* |
| **`Ctrl+S`** | **Rechercher sur YouTube** le terme saisi dans la barre du haut *(30 résultats ; prend en charge `chaîne/` et `chaîne/sujet`)* |
| **`Alt+F`** *(ou `Ctrl+O`)* | **Choisir un filtre de recherche** *(Pertinence, Aujourd'hui, Semaine, Mois, Année, Plus vues, Courtes, Moyennes, Longues, Direct)* |
| **`Alt+M`** *(ou `Ctrl+E`)* | **Charger +30 résultats** pour la recherche en cours *(pagination par 30)* |
| **`Alt+I`** *(ou `Ctrl+T`)* | Regarder **dans le terminal** en vrais pixels (`--vo=sixel` / `--vo=kitty`) |
| **`Alt+B`** | Regarder dans le terminal en **blocs TrueColor** (`--vo=tct`) |
| **`Alt+A`** | Lire **l'audio seul** avec le **visualiseur de spectre Cava 60 FPS** |
| **`Alt+W`** | Forcer l'ouverture dans la **fenêtre MPV** *(utile en mode musique)* |
| **`Alt+D`** | Télécharger la **vidéo (MP4)** ou **l'audio (MP3)** dans `~/Videos/omayt` |
| **`Alt+L`** | Copier le lien de la vidéo dans le presse-papiers (`wl-copy`) |
| **`Ctrl+H`** | Ouvrir l'**Historique** des vidéos regardées |
| **`Ctrl+F`** | Activer/désactiver un filtre local sur la liste en cours |
| **`Esc` / `Ctrl+C`** | Retour au menu principal *(ou quitter)* |

### Lecteur de musique (visualiseur Cava)

| Touche | Action |
| :--- | :--- |
| **`Space`** | Lecture / Pause |
| **`←` / `→`** | Avancer / reculer de 5 secondes |
| **`↑` / `↓`** | Augmenter / baisser le volume |
| **`m`** | Couper / rétablir le son |
| **`v`** | Changer de style de visualiseur *(Classic Bars / Stereo Mirror / Center Symmetrical)* |
| **`q` / `Esc`** | Retour à la TUI |

---

## 🗂️ Stockage local

`omayt` ne télécharge pas les vidéos sur le disque en streaming ; seuls les métadonnées, l'historique et les vignettes en cache sont stockés localement :

- **`~/.cache/omayt/thumbs_hd/`** : cache des vignettes `.jpg` et des versions `.sixel` pré-encodées.
- **`~/.cache/omayt/videos_db.json`**, **`last_list.json`**, **`state.json`** : métadonnées des vidéos et état de la dernière session/recherche.
- **`~/.config/omayt/watch_history.json`** : historique local des vidéos regardées (`Ctrl+H`).
- **`~/.config/omayt/search_history.json`** : historique des recherches récentes affiché dans le menu principal.
- **`~/Videos/omayt/`** : dossier de téléchargement MP4/MP3 (créé uniquement lors d'un téléchargement avec `Alt+D`).

Vous pouvez gérer et vider le cache ou l'historique depuis le menu **`[7] Paramètres & diagnostics`**, ou manuellement avec :

```bash
rm -rf ~/.cache/omayt ~/.config/omayt
```

---

## 📄 Licence

Distribué sous licence [MIT](./LICENSE).
