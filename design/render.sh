#!/bin/bash
# design/cards.html の各カードを 2 倍の PNG にして assets/ に書き出す。
# 使い方: bash design/render.sh            （全部）
#         bash design/render.sh hero       （1枚だけ）
set -euo pipefail
cd "$(dirname "$0")"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="../assets"
mkdir -p "$OUT"

# id 幅 高さ
CARDS="
hero 900 470
sh-who 900 84
sh-pick 900 84
sh-lineup 900 84
sh-journey 900 84
sh-career 900 84
sh-skills 900 84
sh-rules 900 84
sh-links 900 84
pick-unchikun 440 232
pick-notepad 440 232
pick-travel 440 232
pick-oshi 440 232
lineup 900 330
journey 900 288
skills 900 276
btn-site 230 70
btn-x 230 70
btn-youtube 230 70
btn-instagram 230 70
btn-tiktok 230 70
btn-qiita 230 70
btn-income 230 70
btn-apps 230 70
footer 900 190
"

echo "$CARDS" | while read -r id w h; do
  [ -z "$id" ] && continue
  if [ $# -gt 0 ] && [ "$1" != "$id" ]; then continue; fi
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 \
    --default-background-color=00000000 --virtual-time-budget=8000 \
    --window-size="$w,$h" --screenshot="$OUT/$id.png" \
    "file://$PWD/cards.html?c=$id" >/dev/null 2>&1
  echo "$OUT/$id.png"
done
