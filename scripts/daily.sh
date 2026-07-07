#!/usr/bin/env bash
# Daily news radio runner for cron/local automation.
# Usage: ./scripts/daily.sh [news_text_file]
# Default input: /tmp/news_radio_input.txt

set -euo pipefail

INPUT="${1:-/tmp/news_radio_input.txt}"

if [[ ! -f "$INPUT" ]]; then
  echo "Error: input file not found: $INPUT" >&2
  exit 1
fi

exec python -m news_radio --async "$INPUT"
