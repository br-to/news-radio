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

## 完全自動実行（推奨）

```bash
python -m news_radio
```

これだけで:
1. Brave Search で AI / blockchain / prediction market のニュース収集
2. NotebookLM で音声生成（15〜20 分待機）
3. Discord に MP3 投稿 + 進捗・エラー通知

## OpenClaw での設定

Cowork ではなく **cron** を使う。OpenClaw 時代と同じ完全自動化がこれで再現できる。

```bash
openclaw cron add \
  --name "News Radio" \
  --cron "0 7 * * *" \
  --tz "Asia/Tokyo" \
  --session isolated \
  --message "cd /path/to/news-radio && source .env && python -m news_radio"
```

または `scripts/daily.sh` を cron に登録:

```bash
0 7 * * * /path/to/news-radio/scripts/daily.sh >> /tmp/news-radio.log 2>&1
```

### Cowork が向かない理由

- 15〜20 分の `--wait` でセッションが切れる
- notebooklm 認証はローカルマシンに紐づく
- web_search 手動ステップは不要（Brave Search API で代替済み）

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
