#!/usr/bin/env bash
# Install macOS launchd job for daily news radio.
# Usage: ./scripts/install-macos.sh

set -euo pipefail

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
echo "Test now: $SCRIPT_DIR/daily.sh"
