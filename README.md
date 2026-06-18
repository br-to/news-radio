# news-radio

毎朝のニュースを NotebookLM の Audio Overview 機能でラジオ風音声に変換し、Discord に投稿するツール。

## アーキテクチャ

```
[ニューステキスト入力]
 |
 v
[notebooklm CLI] --- Audio Overview (SHORT, 5-7分) を生成
 |
 v
[Discord Webhook] --- 生成した音声ファイルを投稿
```

## 技術スタック

- Python 3.12
- [notebooklm CLI](https://github.com/teng-lin/notebooklm-py) - NotebookLM CLI クライアント (`pip install notebooklm-py`)
- Discord Webhook - 音声ファイルの配信

## ディレクトリ構成

```
news-radio/
├── src/
│   └── news_radio/
│       ├── __init__.py
│       ├── __main__.py      # python -m news_radio 用
│       ├── main.py          # エントリーポイント (テキスト → 音声 → 投稿)
│       ├── audio.py         # NotebookLM CLI で Audio Overview 生成
│       └── discord.py       # Discord Webhook 投稿
├── pyproject.toml
├── .gitignore
└── README.md
```

## 前提条件

- Python 3.12 以上
- `notebooklm` CLI がインストール済み・認証済み
- Discord Webhook URL

## セットアップ

```bash
git clone https://github.com/br-to/news-radio.git
cd news-radio
pip install -e .
```

### notebooklm CLI 認証

```bash
pip install notebooklm-py
notebooklm auth login
```

もしくは手動で storage_state.json を配置する。詳細は notebooklm-py のドキュメントを参照。

## 環境変数

| 変数名 | 説明 |
|--------|------|
| `DISCORD_WEBHOOK_URL` | 音声投稿先の Discord Webhook URL |

## 使い方

```bash
# ファイルから読み込み
python -m news_radio news.txt

# stdin から読み込み
echo "Today's news..." | python -m news_radio

# Python から呼び出し
from news_radio.main import run
await run(news_text)
```

## notebooklm CLI コマンド (内部で使用)

```bash
# ノートブック作成
notebooklm create "News Radio" --json

# ソース追加
notebooklm source add ./news_input.txt --title "Today's News"

# Audio Overview 生成 (SHORT, 日本語, 完了待ち)
notebooklm generate audio --length short --language ja --wait --timeout 900 --retry 2

# 音声ダウンロード
notebooklm download audio ./output.mp3 --latest --force

# ノートブック削除
notebooklm delete <notebook_id> --confirm
```

## ライセンス

MIT
