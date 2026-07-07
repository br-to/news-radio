#!/bin/bash
# 毎朝の news-radio 自動実行ラッパー。launchd から呼ばれる想定。
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

# launchd はログインシェルの PATH を引き継がないため、
# notebooklm CLI (uv tool でインストール, ~/.local/bin) を明示的に通す。
export PATH="$HOME/.local/bin:/opt/homebrew/bin:$PATH"

if [ -f "$PROJECT_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$PROJECT_DIR/.env"
  set +a
fi

exec "$PROJECT_DIR/.venv/bin/news-radio-auto"
