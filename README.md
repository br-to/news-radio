# news-radio

毎朝のニュースを NotebookLM の Audio Overview 機能でラジオ風音声に変換するツール。

## アーキテクチャ

```
[ニューステキスト入力]
 |
 v
[notebooklm CLI] --- Audio Overview (DEFAULT, brief format) を生成
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
├── SKILL.md
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

### 初回ノートブック作成

```bash
notebooklm create "News Radio" --json
notebooklm use <notebook_id>
```

## 使い方

```bash
# ファイルから読み込み
python -m news_radio news.txt

# stdin から読み込み
echo "Today's news..." | python -m news_radio
```

## 音声スタイル

`--format brief` + プロンプト指示で落ち着いたトーンで生成。
大袈裟なリアクションを抑えた淡々としたニュース解説形式。

## ライセンス

MIT
