<div align="center">

# 󰗃 omayt — Omarchy YouTube TUI

**Cliente de YouTube para terminal rápido, visual e sem API — feito sob medida para o ecossistema [Omarchy Linux](https://omarchy.org).**

[![Version](https://img.shields.io/badge/version-v1.3.0-89b4fa?style=for-the-badge)](https://github.com/sabb4th/omayt/releases)
[![Platform](https://img.shields.io/badge/platform-Omarchy%20%7C%20Arch%20Linux-a6e3a1?style=for-the-badge)](https://omarchy.org)
[![Python](https://img.shields.io/badge/python-Zero%20pip%20deps-94e2d5?style=for-the-badge)](./omayt)
[![Graphics](https://img.shields.io/badge/thumbnails-Sixel%20HD%20%C2%B7%20Kitty-f5c2e7?style=for-the-badge)](./omayt)
[![Audio](https://img.shields.io/badge/audio-Cava%20FFT%2060%20FPS-fab387?style=for-the-badge)](./omayt)
[![License](https://img.shields.io/badge/license-MIT-f9e2af?style=for-the-badge)](./LICENSE)

[Destaques](#-o-que-ele-tem-de-melhor) • [Modos de Reprodução](#-4-modos-de-reprodução) • [Instalação](#-dependências--instalação) • [CLI](#-como-usar-cli) • [Atalhos](#-atalhos) • [Armazenamento](#-armazenamento-local)

<br />

<img src="assets/preview.png" alt="omayt v1.3.0 — Menu Principal no Omarchy Linux com tema Catppuccin" width="100%" />

*Menu Principal interativo do `omayt v1.3.0` rodando em janela flutuante no Hyprland / Omarchy com o tema Catppuccin sincronizado automaticamente.*

</div>

---

## Por que o `omayt`?

O **`omayt`** reúne busca no YouTube, thumbnails em alta definição, aceleração de hardware e reprodução de vídeo e música em **um único executável Python**, pensado para funcionar perfeitamente no **Omarchy / Arch Linux** (terminais **Foot**, **Ghostty** e **Kitty**).

| Característica | Como o `omayt` resolve |
| :--- | :--- |
| **Zero chave de API & Zero Invidious** | Pesquisa direta via `yt-dlp` sem depender de quotas da YouTube Data API ou instâncias instáveis do Invidious. |
| **Zero dependências `pip`** | Escrito integralmente em Python padrão do sistema — sem `venv`, sem pacotes extras no PyPI. |
| **Zero bloqueio `HTTP 403`** | Proteção em 3 camadas (*Anti-403*) com bypass do perfil `tv_samsung`, `Ad-Wait Guard` e auto-reconnect. |
| **Zero engasgos por AV1 em CPU** | Exclui streams AV1 (`[vcodec!^=av01]`) e prioriza **H.264 / VP9** com decodificação **VA-API** na GPU. |
| **Zero `cava` externo necessário** | Visualizador de espectro **FFT Radix-2 a 60 FPS** embutido diretamente no player de áudio. |

---

## ✨ O que ele tem de melhor

### 🎨 Menu Principal Artesanal & Sincronia Nativa com Temas do Omarchy
- **Interface sem flicker:** Renderização em tela alternativa com atualização sincronizada (`\033[?2026h`), logo pixel-art `OMAYT` com gradiente TrueColor animado, mini-equalizadores, barra de status ao vivo (tema ativo, `VA-API`, `Anti-403`, contador do histórico) e últimas buscas recentes.
- **Paleta automática do Omarchy:** Lê `~/.local/state/omarchy/current/theme/colors.toml` e `theme.name` na inicialização e aplica as cores exatas do seu tema no Menu Principal, no explorador `fzf`, no painel de preview e no visualizador Cava.
- **Navegação em 1 tecla:** Pressione `1–7` para abrir qualquer módulo direto ou `/` para iniciar uma busca imediata no YouTube.

### 🎵 Modo Música com Visualizador de Espectro Cava 60 FPS Embutido
- **Captura de áudio real do sistema:** Lê o monitor de saída em baixa latência (`18ms`) via **PipeWire** (`pw-record`) ou **PulseAudio** (`parec` em `@DEFAULT_MONITOR@`).
- **Motor FFT Radix-2 em Python puro:** 512 amostras com janela de Hann, AGC dinâmico, física de gravidade, filtro *Monstercat* e *Peak Caps* flutuantes.
- **3 estilos visuais ao vivo (`v`):**
  1. **Cava Classic Bars** *(barras verticais com gradientes do tema e Peak Caps)*
  2. **Stereo Mirror (Monstercat)** *(espectro espelhado L/R a partir do centro)*
  3. **Center Symmetrical** *(graves centralizados com agudos nas bordas)*
- **Controle IPC do `mpv`:** Barra de progresso em tempo real, play/pause (`Espaço`), seek ±5s (`←/→`), volume (`↑/↓`) e mute (`m`) sem sair do terminal.

### 🖼️ Thumbnails HD (Sixel & Kitty Graphics Protocol)
- **Prefetch paralelo assíncrono:** Baixa miniaturas em background (`ThreadPoolExecutor` com 10 workers) direto do CDN oficial (`i.ytimg.com` — `maxresdefault.jpg`, com fallback para `sddefault` e `hqdefault`).
- **Dimensionamento exato em pixels:** Consulta `TIOCGWINSZ` para calcular a largura ideal da miniatura até `1152px` (`1280px` no modo Sixel direto) com proporção 16:9 exata.
- **Fix definitivo para Arch Linux (`gdk-pixbuf2` / `glycin`):** No Arch recente, o utilitário `/usr/bin/img2sixel` pode falhar retornando `0 bytes`. O `omayt` contorna o problema decodificando a imagem com `ffmpeg` (crop 16:9 + escala **Lanczos** + nitidez `unsharp`) e invocando `sixel_encoder_encode_bytes` em memória diretamente na `libsixel.so.1` via `ctypes`, com cache `.sixel` em disco.
- **Multi-terminal:** Usa `kitten icat` (`--transfer-mode=memory --unicode-placeholder`) no **Kitty** e **Ghostty**, Sixel HD nativo no **Foot**, e fallback automático para `chafa`.

### ⚡ Aceleração de Hardware VA-API & Exclusão de AV1
- Prioriza streams **H.264 / VP9** (`[vcodec!^=av01]`) até **1080p** na janela `mpv` (`--hwdec=vaapi,vaapi-copy`) e até **720p** nos modos inline do terminal (`--hwdec=vaapi-copy`).
- Evita decodificação pesada de AV1 em software e contorna falhas comuns do Vulkan Video (`VK_KHR_video_decode_queue`) em GPUs Intel Iris Xe, AMD e Mesa.

### 🛡️ Proteção Tripla Anti-403 (`tv_samsung` Bypass + `Ad-Wait Guard`)
1. **Bypass do cliente `tv_samsung`:** Injeta `--extractor-args "youtube:player_client=default,-tv_samsung"` no `yt-dlp` e no `mpv` (`--ytdl-raw-options-append`).
2. **Interceptador `Ad-Wait Guard` no `ytdl_hook` do `mpv`:** O `omayt` atua como wrapper do `yt-dlp`, inspeciona o campo `available_at` dos streams retornados no JSON e aguarda a liberação exata com uma contagem regressiva visual no terminal antes de entregar a URL ao `ffmpeg`.
3. **Auto-Reconnect HTTP 4xx:** Configura `--stream-lavf-o=reconnect=1,reconnect_streamed=1,reconnect_on_http_error=4xx,reconnect_delay_max=5` e retry automático caso o stream seja retido nos primeiros segundos.

<details>
<summary><strong>Por que o erro HTTP 403 Forbidden acontece em clientes tradicionais?</strong></summary>

Clientes de terminal tradicionais (`ytfzf` ou `mpv` puro) frequentemente falham com `HTTP 403 Forbidden` porque o `yt-dlp` usa por padrão o perfil `tv_samsung` (Smart TV), no qual o YouTube aplica uma janela de espera de ~3 a 5 segundos (`available_at`) simulando o tempo de "pular anúncio". Enquanto o `yt-dlp` em modo download aguarda esse intervalo, o `mpv` extrai o JSON via `yt-dlp -J` e tenta abrir a URL imediatamente no `ffmpeg`, recebendo `403 Forbidden`. As 3 camadas do `omayt` eliminam esse problema na raiz.

</details>

### 🔎 Busca por Canal (`canal/`), Filtros de Pesquisa (`Alt+F`), Paginação & Diagnóstico
- **Busca exclusiva de canal (`canal/`):** Digite `nome/` (ex.: `raimundo/`) para listar **somente os vídeos daquele canal** (do mais recente em diante, com paginação +30), ou `nome/termo` (ex.: `raimundo/bitcoin`) para pesquisar dentro do canal.
- **Filtros de pesquisa (`Alt+F`):** Pressione `Alt+F` (ou `Ctrl+O`) na TUI — ou `Tab` / `Alt+F` no modal de busca — para filtrar por **Hoje**, **Esta semana**, **Este mês**, **Este ano**, **Mais vistos**, **Curtos (< 3 min)**, **Médios (3–20 min)**, **Longos (> 20 min)** ou **Ao vivo**.
- **Paginação 30 em 30:** Cada pesquisa carrega 30 resultados e permite expandir **+30 resultados** sob demanda (`Alt+M`, `Ctrl+E` ou selecionando o item ao final da lista), preservando a ordem e a posição do cursor.
- **Link / URL Direta (`[5]`):** Suporta URLs completas (`youtube.com/watch`, `youtu.be`, `shorts`, `live`, `embed`) ou IDs de 11 caracteres, com **auto-detecção da área de transferência** via `wl-paste` e escolha de player (*Janela MPV*, *Terminal Sixel/Kitty*, *Cava* ou *Download*).
- **Downloads & Biblioteca Offline (`Alt+D` / `[6]`):** Baixe vídeos em **MP4 (1080p H.264/VP9)** ou apenas áudio em **MP3** para `~/Videos/omayt/` e reproduza os arquivos locais diretamente pelo menu.
- **Configurações & Diagnóstico (`[7]`):** Verifica todas as dependências do sistema, exibe swatches da paleta Omarchy ativa, mostra estatísticas de cache HD/histórico e permite aplicar otimizações (`f`) ou limpar cache/buscas (`c` / `h`) em um toque.
- **Migração automática do `ytfzf`:** Importa automaticamente seu histórico existente de `~/.cache/ytfzf/watch_hist` na primeira execução caso o histórico do `omayt` ainda esteja vazio.

---

## 🎬 4 Modos de Reprodução

| Modo | Atalho na TUI | Motor / Protocolo | Qualidade & HWDec | Melhor para |
| :--- | :--- | :--- | :--- | :--- |
| **Janela MPV** | `Enter` *(ou `Alt+W`)* | `mpv` nativo (Wayland) | Até **1080p** · `vaapi,vaapi-copy` | Assistir em tela cheia ou janela flutuante com aceleração de GPU |
| **Vídeo Inline em Pixels** | `Alt+I` *(ou `Ctrl+T`)* | `mpv --vo=sixel` *(Foot)* / `--vo=kitty` *(Kitty/Ghostty)* | Até **720p** · `vaapi-copy` | Assistir dentro da própria janela do terminal em pixels reais |
| **Blocos TrueColor** | `Alt+B` | `mpv --vo=tct` | Até **720p** · `vaapi-copy` | Compatibilidade universal com qualquer terminal TrueColor |
| **Modo Música + Cava** | `Alt+A` *(ou `[4]` no Menu)* | `mpv --no-video` + IPC + FFT 60 FPS | `bestaudio/best` | Ouvir músicas e podcasts com visualizador de espectro ao vivo |

---

## 📦 Dependências & Instalação

### Dependências no Omarchy / Arch Linux

- **Obrigatórias:** `python` (Python 3 do sistema), `fzf` (`>= 0.50`), `yt-dlp`, `mpv`, `ffmpeg`, `libsixel`
- **Opcionais (recomendadas):** `wl-clipboard` (copiar/colar links no Wayland), `libnotify` (notificações ao copiar link), `chafa` (fallback gráfico) e PipeWire/PulseAudio (`pw-record` ou `parec`) para o visualizador Cava.

```bash
omarchy pkg add fzf yt-dlp mpv ffmpeg libsixel
```

### Opção 1: Script Instalador (`install.sh`)

```bash
git clone https://github.com/sabb4th/omayt.git
cd omayt
chmod +x install.sh omayt
./install.sh
```

O `install.sh` executa 3 passos automaticamente:
1. Instala o executável em `~/.local/bin/omayt`;
2. Configura `~/.config/yt-dlp/config` com `--extractor-args "youtube:player_client=default,-tv_samsung"`;
3. Configura `~/.config/ytfzf/conf.sh` e `~/.config/ytfzf/thumbnail-viewers/sixel-inline` para usar o renderizador Sixel do `omayt` (`omayt --sixel`).

### Opção 2: Pacote Arch Linux (`PKGBUILD`)

```bash
makepkg -si
```

---

## 🚀 Como Usar (CLI)

```bash
# Abrir o Menu Principal interativo
omayt

# Pesquisar direto no YouTube (30 resultados iniciais + thumbnails HD)
omayt "omarchy linux"

# Listar somente os vídeos de um canal específico (ou pesquisar dentro dele)
omayt "raimundo/"
omayt "raimundo/bitcoin"

# Pesquisar com filtro direto pela CLI (today, week, month, year, views, short, medium, long, live)
omayt --filter views "omarchy linux"

# Pular o menu inicial e abrir direto no explorador TUI (fzf)
omayt --no-menu
omayt -t

# Abrir direto no Histórico de vídeos assistidos
omayt -H
omayt --history

# Aplicar otimizações globais Anti-403, sem AV1 e VA-API em yt-dlp e mpv
omayt --fix-ytdlp

# Renderizar qualquer imagem em Sixel HD no terminal Foot
omayt --sixel caminho/para/imagem.jpg 640

# Exibir versão ou ajuda
omayt -v
omayt -h
```

### 🌍 Idioma da interface

A interface vem em **português do Brasil**, **inglês** e **francês** — menu principal, rótulos do `fzf`, painel de preview, faixas dos players e `--help`. De primeira, o app acompanha automaticamente o **idioma do Omarchy** (`~/.config/omarchy/language`) e pode ser alternado a qualquer momento em **[7] Ajustes & diagnóstico** (`[e]` English, `[p]` Português (Brasil), `[l]` alternar). Ordem de prioridade:

1. `OMAYT_LANG` (`en`, `pt`, `fr`, além de `pt_BR`, `pt-PT`, `fr_FR`, `fr-CA`…), que sempre tem prioridade;
2. o idioma salvo em **[7] Ajustes & diagnóstico** (`~/.config/omayt/settings.json`);
3. o **idioma do Omarchy** (`~/.config/omarchy/language` — se estiver em `pt-BR`, começa em português; se estiver em inglês, começa em inglês);
4. a locale do sistema (`LC_ALL` / `LC_MESSAGES` / `LANG`);
5. inglês caso contrário.

```bash
# Apenas um lançamento, sem alterar o ajuste salvo
OMAYT_LANG=fr omayt
```

---

## ⌨️ Atalhos

### Menu Principal

| Tecla | Ação |
| :--- | :--- |
| **`↑` / `↓`** ou **`j` / `k`** | Navegar entre as opções |
| **`Enter`** | Abrir o item selecionado |
| **`/`** | Abrir busca rápida no YouTube |
| **`1` – `7`** | Acesso direto aos módulos do menu |
| **`0` / `q` / `Esc`** | Sair do `omayt` |

### Explorador TUI (`fzf`)

| Atalho | Ação |
| :--- | :--- |
| **`Enter`** | Assistir no **`mpv`** *(ou tocar no Cava no Modo Música; busca na 1ª linha `` / carrega +30 na última linha `󰐕`)* |
| **`Ctrl+S`** | **Pesquisar no YouTube** o termo digitado na barra superior *(30 resultados; suporta `canal/` e `canal/termo`)* |
| **`Alt+F`** *(ou `Ctrl+O`)* | **Alterar filtro de pesquisa** *(Relevância, Hoje, Semana, Mês, Ano, Mais vistos, Curtos, Médios, Longos, Ao vivo)* |
| **`Alt+M`** *(ou `Ctrl+E`)* | **Carregar +30 resultados** para a busca atual *(paginação 30 em 30)* |
| **`Alt+I`** *(ou `Ctrl+T`)* | Assistir **dentro do terminal** em pixels reais (`--vo=sixel` / `--vo=kitty`) |
| **`Alt+B`** | Assistir dentro do terminal em **blocos TrueColor** (`--vo=tct`) |
| **`Alt+A`** | Tocar **apenas áudio** com **visualizador de espectro Cava 60 FPS** |
| **`Alt+W`** | Forçar abertura na **janela MPV** *(útil quando no Modo Música)* |
| **`Alt+D`** | Baixar **vídeo (MP4)** ou **áudio (MP3)** para `~/Videos/omayt` |
| **`Alt+L`** | Copiar o link do vídeo para o clipboard (`wl-copy`) |
| **`Ctrl+H`** | Abrir o **Histórico** de vídeos assistidos |
| **`Ctrl+F`** | Alternar filtro local na lista atual |
| **`Esc` / `Ctrl+C`** | Voltar ao Menu Principal *(ou sair)* |

### Player de Música (Visualizador Cava)

| Tecla | Ação |
| :--- | :--- |
| **`Espaço`** | Play / Pause |
| **`←` / `→`** | Avançar / Retroceder 5 segundos |
| **`↑` / `↓`** | Aumentar / Diminuir volume |
| **`m`** | Ativar / Desativar mudo |
| **`v`** | Alternar estilo do visualizador *(Classic Bars / Stereo Mirror / Center Symmetrical)* |
| **`q` / `Esc`** | Voltar à TUI |

---

## 🗂️ Armazenamento Local

O `omayt` não baixa vídeos em disco ao assistir via streaming; apenas metadados, histórico e miniaturas em cache são armazenados localmente:

- **`~/.cache/omayt/thumbs_hd/`**: Cache das miniaturas `.jpg` e versões pré-codificadas `.sixel`.
- **`~/.cache/omayt/videos_db.json`**, **`last_list.json`**, **`state.json`**: Metadados dos vídeos e estado da última sessão/busca.
- **`~/.config/omayt/watch_history.json`**: Histórico local dos vídeos assistidos (`Ctrl+H`).
- **`~/.config/omayt/search_history.json`**: Histórico das pesquisas recentes exibidas no Menu Principal.
- **`~/Videos/omayt/`**: Pasta de downloads MP4/MP3 (criada apenas ao baixar com `Alt+D`).

Você pode gerenciar e limpar cache ou histórico pelo menu **`[7] Configurações & Diagnóstico`** ou manualmente com:

```bash
rm -rf ~/.cache/omayt ~/.config/omayt
```

---

## 📄 Licença

Distribuído sob a licença [MIT](./LICENSE).
