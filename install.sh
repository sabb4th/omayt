#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"

echo "󰗃 Installing omayt (Omarchy YouTube TUI)..."

# 1. Install the omayt binary into ~/.local/bin/omayt
mkdir -p "$BIN_DIR"
chmod +x "$PROJECT_DIR/omayt"
cp -f "$PROJECT_DIR/omayt" "$BIN_DIR/omayt"
chmod +x "$BIN_DIR/omayt"
echo "  ✓ Binary installed at: $BIN_DIR/omayt"

# 2. Configure the global yt-dlp fix (avoids the HTTP 403 ad block on the tv_samsung client)
mkdir -p "$HOME/.config/yt-dlp"
YTDLP_CONFIG="$HOME/.config/yt-dlp/config"
if ! grep -q -- "-tv_samsung" "$YTDLP_CONFIG" 2>/dev/null; then
    if [ -s "$YTDLP_CONFIG" ]; then
        YTDLP_BACKUP="$YTDLP_CONFIG.bak.$(date +%s)"
        cp -p "$YTDLP_CONFIG" "$YTDLP_BACKUP"
        echo "  ✓ Your existing yt-dlp config was backed up to: $YTDLP_BACKUP"
    fi
    {
        echo ""
        echo "# Avoids the 5s HTTP 403 ad block on the tv_samsung client"
        echo '--extractor-args "youtube:player_client=default,-tv_samsung"'
    } >> "$YTDLP_CONFIG"
    echo "  ✓ tv_samsung client fix applied to: $YTDLP_CONFIG"
else
    echo "  ✓ tv_samsung client fix already present in: $YTDLP_CONFIG"
fi

# 3. Also configure Sixel thumbnails + the tv_samsung fix in ytfzf (if you use ytfzf)
mkdir -p "$HOME/.config/ytfzf/thumbnail-viewers"
cat << 'EOF' > "$HOME/.config/ytfzf/thumbnail-viewers/sixel-inline"
#!/usr/bin/env sh
case "$1" in
    view)
        thumb_path="$2"
        preview_cols="${7:-${5:-40}}"
        [ ! -f "$thumb_path" ] && exit 0
        px_w=$(( preview_cols * 7 ))
        [ "$px_w" -lt 220 ] && px_w=280
        [ "$px_w" -gt 480 ] && px_w=480
        printf "\n"
        if [ -x "$HOME/.local/bin/omayt" ]; then
            "$HOME/.local/bin/omayt" --sixel "$thumb_path" "$px_w" 2>/dev/null
        elif command -v chafa >/dev/null 2>&1; then
            chafa -s "${preview_cols}x$(( ${8:-20} / 2 ))" "$thumb_path" 2>/dev/null
            printf "\n"
        fi
        ;;
esac
EOF
chmod +x "$HOME/.config/ytfzf/thumbnail-viewers/sixel-inline"

YTFZF_CONF="$HOME/.config/ytfzf/conf.sh"
if [ -e "$YTFZF_CONF" ]; then
    echo "  ! $YTFZF_CONF already exists — left untouched."
    echo "    To use omayt's Sixel thumbnail viewer and the tv_samsung fix in ytfzf, add these lines to it:"
    echo "      thumbnail_viewer=\"\$HOME/.config/ytfzf/thumbnail-viewers/sixel-inline\""
    echo "      url_handler_opts='--ytdl-raw-options-append=extractor-args=\"youtube:player_client=default,-tv_samsung\"'"
else
cat << 'EOF' > "$YTFZF_CONF"
show_thumbnails=1
fzf_preview_side="left"
preview_window_width="50%"
thumbnail_viewer="$HOME/.config/ytfzf/thumbnail-viewers/sixel-inline"
url_handler_opts='--ytdl-raw-options-append=extractor-args="youtube:player_client=default,-tv_samsung"'

download_thumbnails() {
    [ "$skip_thumb_download" -eq 1 ] && return 0
    curl_config_file="${session_temp_dir}/curl_config"
    [ -z "$*" ] && return 0
    : >"$curl_config_file"
    for line in "$@"; do
        video_id="${line##*';'}"
        thumb_url="https://i.ytimg.com/vi/${video_id}/hqdefault.jpg"
        printf "url=\"%s\"\noutput=\"%s/%s.jpg\"\n" "$thumb_url" "$thumb_dir" "$video_id"
    done >>"$curl_config_file"
    curl -s -fLZ -K "$curl_config_file"
}

thumbnail_video_info_text() {
    [ -n "$title" ] && printf "\n ${c_bold}${c_cyan}%s${c_reset}" "$title"
    [ -n "$channel" ] && printf "\n ${c_blue}Channel  ${c_green}%s${c_reset}" "$channel"
    [ -n "$duration" ] && printf "\n ${c_blue}Duration ${c_yellow}%s${c_reset}" "$duration"
    [ -n "$views" ] && printf "\n ${c_blue}Views    ${c_magenta}%s${c_reset}" "$views"
    [ -n "$date" ] && printf "\n ${c_blue}Date     ${c_cyan}%s${c_reset}\n" "$date"
}
EOF
    echo "  ✓ Sixel thumbnail configuration + tv_samsung fix applied to ytfzf (~/.config/ytfzf/conf.sh)"
fi

echo ""
echo "🎉 Installation complete! Now just run:"
echo "   omayt"
echo "   or: omayt \"your search\""
