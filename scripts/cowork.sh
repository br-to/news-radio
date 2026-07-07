#!/usr/bin/env bash
# Cowork から呼ぶ用: /tmp/news_radio_input.txt → NotebookLM → Discord
#
# 前提: Cowork が Step 1-2（web_search + ファイル保存）を済ませていること
#
# Usage:
#   ./scripts/cowork.sh           # 同期（MP3 まで待つ）
#   ./scripts/cowork.sh --async   # 非同期（セッション切れ対策）

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
INPUT="/tmp/news_radio_input.txt"

if [[ -f "$PROJECT_DIR/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$PROJECT_DIR/.env"
  set +a
fi

if [[ ! -f "$INPUT" ]]; then
  echo "Error: $INPUT not found. Cowork でニュース収集・保存を先に実行してください。" >&2
  exit 1
fi

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

cd "$PROJECT_DIR"

if [[ "${1:-}" == "--async" ]]; then
  exec "$PYTHON" -m news_radio --async "$INPUT"
else
  exec "$PYTHON" -m news_radio "$INPUT"
fi
