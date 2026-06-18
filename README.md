# News Radio

毎朝自動でニュースを収集し、NotebookLM の Audio Overview 機能を使って音声ニュース番組を生成、Discord に投稿するボットです。

## 構成図

```
cron (毎朝 7:00 JST)
  |
  v
[Brave Search API] --- ニュース記事を検索・取得
  |
  v
[notebooklm-py] --- 記事を元に Audio Overview (音声) を生成
  |
  v
[Discord Webhook] --- 生成した音声ファイルを投稿
```

## 技術スタック

- Python 3.12
- [notebooklm-py](https://github.com/nichochar/notebooklm-py) - 非公式 NotebookLM API クライアント
- Brave Search API - ニュース検索
- Discord Webhook - 音声ファイルの配信

## ディレクトリ構成

```
news-radio/
├── src/
│   └── news_radio/
│       ├── __init__.py
│       ├── main.py          # エントリーポイント
│       ├── search.py        # Brave Search によるニュース取得
│       ├── audio.py         # NotebookLM Audio Overview 生成
│       └── discord.py       # Discord Webhook 投稿
├── pyproject.toml
├── .gitignore
└── README.md
```

## セットアップ

### 前提条件

- Python 3.12 以上
- 各種 API キー

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/br-to/news-radio.git
cd news-radio

# 依存関係のインストール
pip install -e .
```

### 環境変数

以下の環境変数を設定してください:

| 変数名 | 説明 |
|--------|------|
| `BRAVE_API_KEY` | Brave Search API キー |
| `GOOGLE_ACCESS_TOKEN` | Google アカウントのアクセストークン (NotebookLM 用) |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL |

### 実行

```bash
# 手動実行
python -m news_radio

# cron 設定例 (毎朝 7:00 JST = 22:00 UTC 前日)
0 22 * * * cd /path/to/news-radio && python -m news_radio
```

## ライセンス

MIT
