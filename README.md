# News Radio

毎朝自動でニュースを収集し、NotebookLM の Audio Overview 機能を使ってラジオ風音声を生成、Discord に投稿するツールです。

## 構成図

```
cron (毎朝 7:00 JST)
  |
  v
[Discord API] --- ニュースチャンネルから最新投稿を取得
  |
  v
[notebooklm-py] --- ニュースを元に Audio Overview (音声) を生成
  |
  v
[Discord Webhook] --- 生成した音声ファイルを投稿
```

## 技術スタック

- Python 3.12
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) - 非公式 NotebookLM API クライアント
- Discord API - ニュース取得元
- Discord Webhook - 音声ファイルの配信

## ディレクトリ構成

```
news-radio/
├── src/
│   └── news_radio/
│       ├── __init__.py
│       ├── __main__.py      # python -m news_radio 用
│       ├── main.py          # エントリーポイント
│       ├── search.py        # Discord チャンネルからニュース取得
│       ├── audio.py         # NotebookLM Audio Overview 生成
│       └── discord.py       # Discord Webhook 投稿
├── pyproject.toml
├── .gitignore
└── README.md
```

## セットアップ

### 前提条件

- Python 3.12 以上
- Discord Bot トークン
- Google アカウント (NotebookLM 用)

### インストール

```bash
git clone https://github.com/br-to/news-radio.git
cd news-radio
pip install -e .
```

### 環境変数

| 変数名 | 説明 |
|--------|------|
| `DISCORD_BOT_TOKEN` | Discord Bot トークン (ニュース取得用) |
| `NEWS_CHANNEL_ID` | ニュース取得元の Discord チャンネル ID |
| `NEWS_BOT_ID` | ニュース投稿 Bot の ID (フィルタ用、任意) |
| `DISCORD_WEBHOOK_URL` | 音声投稿先の Discord Webhook URL |

### 実行

```bash
# 手動実行
python -m news_radio

# cron 設定例 (毎朝 7:00 JST = 22:00 UTC 前日)
0 22 * * * cd /path/to/news-radio && python -m news_radio
```

## ライセンス

MIT
