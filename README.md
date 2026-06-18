# news-radio

毎朝のニュースを NotebookLM の Audio Overview 機能でラジオ風音声に変換するツール。

## アーキテクチャ

```
[ニューステキスト入力]
 |
 v
[notebooklm CLI] --- Audio Overview (DEFAULT, 10-15分) を生成
 |
 v
[NotebookLM通知] --- 生成完了をプッシュ通知
```

## 技術スタック

- Python 3.12
- [notebooklm CLI](https://github.com/teng-lin/notebooklm-py) - NotebookLM CLI クライアント (`pip install notebooklm-py`)

## ディレクトリ構成

```
news-radio/
├── src/
│   └── news_radio/
│       ├── __init__.py
│       ├── __main__.py      # python -m news_radio 用
│       ├── main.py          # エントリーポイント (テキスト → 音声生成)
│       └── audio.py         # NotebookLM CLI で Audio Overview 生成
├── pyproject.toml
├── .gitignore
└── README.md
```

## 前提条件

- Python 3.12 以上
- `notebooklm` CLI がインストール済み・認証済み

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

### ノートブックのセットアップ（初回のみ）

```bash
notebooklm create "News Radio" --json
notebooklm use <notebook_id>
```

以降の実行では同じノートブックを使い回す。ソースは毎回差し替えられる。

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
# ソース一覧
notebooklm source list

# ソース削除
notebooklm source delete <source_id>

# ソース追加
notebooklm source add ./news_input.txt --title "Today's News"

# Audio Overview 生成 (DEFAULT, 日本語, 完了待ち)
notebooklm generate audio --length default --language ja --wait --timeout 900 --retry 2

# 音声ダウンロード
notebooklm download audio ./output.mp3 --latest --force
```

## ライセンス

MIT
