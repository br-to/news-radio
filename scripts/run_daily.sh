#!/bin/bash
# 毎朝の news-radio 自動実行ラッパー。launchd から呼ばれる想定。
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if [ -f "$PROJECT_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$PROJECT_DIR/.env"
  set +a
fi

exec "$PROJECT_DIR/.venv/bin/news-radio-auto"
