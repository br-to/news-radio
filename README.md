# News Radio

毎朝のニュースを NotebookLM の Audio Overview 機能でラジオ風音声に変換し、Discord に投稿するツール。

## 構成図

```
[ニューステキスト入力]
  |
  v
[notebooklm-py] --- Audio Overview (SHORT, 5-7分) を生成
  |
  v
[Discord Webhook] --- 生成した音声ファイルを投稿
```

## 技術スタック

- Python 3.12
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) - 非公式 NotebookLM API クライアント
- Discord Webhook - 音声ファイルの配信

## ディレクトリ構成

```
news-radio/
├── src/
│   └── news_radio/
│       ├── __init__.py
│       ├── __main__.py      # python -m news_radio 用
│       ├── main.py          # エントリーポイント (テキスト → 音声 → 投稿)
│       ├── audio.py         # NotebookLM Audio Overview 生成
│       └── discord.py       # Discord Webhook 投稿
├── pyproject.toml
├── .gitignore
└── README.md
```

## セットアップ

### 前提条件

- Python 3.12 以上
- Google アカウント (NotebookLM 用)

### インストール

```bash
git clone https://github.com/br-to/news-radio.git
cd news-radio
pip install -e .
```

### 認証 (NotebookLM)

notebooklm-py はブラウザの Google セッション cookie で認証する。

```bash
pip install "notebooklm-py[cookies]"
notebooklm auth login
```

もしくは手動で `storage_state.json` を配置する。詳細は notebooklm-py のドキュメントを参照。

### 環境変数

| 変数名 | 説明 |
|--------|------|
| `NOTEBOOKLM_STORAGE_PATH` | NotebookLM の storage_state.json パス (任意) |
| `DISCORD_WEBHOOK_URL` | 音声投稿先の Discord Webhook URL |

### 使い方

```bash
# ファイルから読み込み
python -m news_radio news.txt

# stdin から読み込み
echo "Today's news..." | python -m news_radio

# Python から呼び出し
from news_radio.main import run
await run(news_text)
```

## ライセンス

MIT
