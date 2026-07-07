#!/usr/bin/env bash
# Full daily automation: Brave Search → NotebookLM → Discord
#
# Setup:
#   1. cp .env.example .env && fill in values
#   2. source .env
#   3. crontab -e:
#      0 7 * * * /path/to/news-radio/scripts/daily.sh >> /tmp/news-radio.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Load env if present
if [[ -f "$PROJECT_DIR/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$PROJECT_DIR/.env"
  set +a
fi

cd "$PROJECT_DIR"

PYTHON=""
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    PYTHON="$candidate"
    break
  fi
done

if [[ -z "$PYTHON" ]]; then
  echo "Error: python3 not found" >&2
  exit 1
fi

exec "$PYTHON" -m news_radio
