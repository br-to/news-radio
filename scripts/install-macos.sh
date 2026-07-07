#!/usr/bin/env bash
# Install macOS launchd job for daily news radio.
#
# Usage:
#   ./scripts/install-macos.sh           # 7:00 実行（スリープ中は起きたときに実行）
#   ./scripts/install-macos.sh --wake    # 6:55 に Mac を自動起動して 7:00 実行

set -euo pipefail

WAKE=false
if [[ "${1:-}" == "--wake" ]]; then
  WAKE=true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PLIST_SRC="$SCRIPT_DIR/com.news-radio.daily.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.news-radio.daily.plist"

if [[ ! -f "$PROJECT_DIR/.env" ]]; then
  echo "Error: $PROJECT_DIR/.env not found. Run: cp .env.example .env" >&2
  exit 1
fi

sed "s|/REPLACE/WITH/PATH/TO/news-radio|$PROJECT_DIR|g" "$PLIST_SRC" > "$PLIST_DST"
launchctl unload "$PLIST_DST" 2>/dev/null || true
launchctl load "$PLIST_DST"

echo "Installed: $PLIST_DST"
echo "Runs daily at 07:00 (Mac local time). Log: /tmp/news-radio.log"
echo ""
echo "スリープ中の挙動:"
echo "  - 7:00 にスリープ中 → 次に Mac を起こしたときに実行される（launchd 標準）"
echo "  - 完全スリープ中に処理することはできない（15-20分の処理のため）"
echo ""

if $WAKE; then
  echo "6:55 に Mac を自動起動するスケジュールを設定します（要 sudo）..."
  sudo pmset repeat wakeorpoweron MTWRFSU 06:55:00
  echo "設定完了。電源接続 + 蓋を閉じた状態でも起動する機種が多いです。"
  echo "解除: sudo pmset repeat cancel"
else
  echo "7:00 前に自動起動したい場合:"
  echo "  ./scripts/install-macos.sh --wake"
fi

echo ""
echo "Test now: $SCRIPT_DIR/daily.sh"
