---
name: news-radio
description: "Fully automated daily news radio: Brave Search → NotebookLM → Discord."
---

# News Radio

毎朝自動でニュースを収集し、NotebookLM で Audio Overview を生成、Discord に投稿する。

## 前提条件

- `notebooklm` CLI インストール済み・認証済み
- ノートブック「News Radio」作成済み (`notebooklm use <id>`)
- `news-radio` インストール済み (`pip install -e .`)
- 環境変数: `BRAVE_API_KEY`, `DISCORD_WEBHOOK_URL`

## 完全自動実行（OpenClaw 不要）

```bash
python -m news_radio
```

## スケジュール実行

**自分の Mac / PC 上で動かす。** OpenClaw は不要。

```bash
# Mac
./scripts/install-macos.sh

# Linux
0 7 * * * /path/to/news-radio/scripts/daily.sh >> /tmp/news-radio.log 2>&1
```

## 手動モード

```bash
# ファイルから
python -m news_radio /tmp/news_radio_input.txt

# 非同期（Discord には開始通知のみ）
python -m news_radio --async news.txt
```

## 環境変数

| 変数 | 説明 |
|------|------|
| `BRAVE_API_KEY` | Brave Search API キー |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL |
| `NEWS_QUERIES` | 検索クエリ（カンマ区切り、省略時は AI/blockchain/prediction market） |

## Discord 通知

| タイミング | 内容 |
|-----------|------|
| 開始 | 📻 ニュース収集中 / 音声生成中 |
| 成功 | 🎙️ MP3 ファイル投稿 |
| 失敗 | ❌ エラーメッセージ |

## 注意事項

- NotebookLM Free は 3回/日
- 生成に 15-20 分かかる（cron の `--wait` は問題なし、バックグラウンドで完走）
- `notebooklm auth login` は実行マシンで1回だけ必要
