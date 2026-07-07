# news-radio

毎朝のニュースを NotebookLM の Audio Overview 機能でラジオ風音声に変換するツール。
Brave Search API でニュースを自動収集し、音声生成後に Discord へ通知する自動実行パイプラインも搭載。

## アーキテクチャ

```
[pmset 自動起床 06:55] → [launchd 07:00起動]
 |
 v
[Brave Search API] --- blockchain/AI/オンチェーン金融/予測市場のニュースを収集
 |
 v
[notebooklm CLI] --- Audio Overview (DEFAULT, brief format) を生成
 |
 v
[Discord Webhook] --- ニュース一覧+音声ファイルを通知
[NotebookLM通知] --- 生成完了をプッシュ通知（アプリ側）
```

自動パイプラインはローカル実行（NotebookLM の認証がローカルのブラウザセッションに
紐づいているため）。Mac がスリープしていても `pmset repeat wake` で自動起床してから
launchd がジョブを起動する。

## 技術スタック

- Python 3.12
- [notebooklm CLI](https://github.com/teng-lin/notebooklm-py) - NotebookLM CLI クライアント (`pip install notebooklm-py`)
- Brave Search API - ニュース収集
- Discord Webhook - 通知
- launchd / pmset (macOS) - 定時自動実行

## ディレクトリ構成

```
news-radio/
├── src/
│   └── news_radio/
│       ├── __init__.py
│       ├── __main__.py      # python -m news_radio 用
│       ├── main.py          # 手動実行エントリーポイント (テキスト → 音声生成)
│       ├── audio.py         # NotebookLM CLI で Audio Overview 生成
│       ├── news.py          # Brave Search API でニュース収集
│       ├── discord.py       # Discord Webhook通知
│       └── pipeline.py      # 自動実行エントリーポイント (収集→生成→通知)
├── scripts/
│   └── run_daily.sh         # launchd から呼ばれるラッパースクリプト
├── pyproject.toml
├── SKILL.md
├── .env.example
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

## 自動実行パイプライン（毎朝7時）

blockchain / AI / オンチェーン金融 / 予測市場のニュースを毎朝自動収集し、
音声化して Discord に通知する。

### 1. 依存関係のインストール

```bash
uv venv --python 3.12 .venv
uv pip install -e . --python .venv/bin/python
```

### 2. API キーの設定

```bash
cp .env.example .env
```

`.env` を編集し、以下を設定する。

- `BRAVE_API_KEY` - [Brave Search API](https://api-dashboard.search.brave.com/) のキー
- `DISCORD_WEBHOOK_URL` - 通知したい Discord チャンネルの Webhook URL

### 3. 動作確認（手動実行）

```bash
./scripts/run_daily.sh
```

### 4. 自動起床の設定（Macがスリープしていても実行するため）

```bash
sudo pmset repeat wake MTWRFSU 06:55:00
```

### 5. launchd への登録（毎朝7:00に自動実行）

`~/Library/LaunchAgents/com.br-to.news-radio.plist` は登録済み。以下のコマンドで
状態確認・再読込ができる。

```bash
# 状態確認
launchctl list | grep news-radio

# 手動でテスト起動（スケジュール前に試したい場合）
launchctl start com.br-to.news-radio

# 設定変更後の再読込
launchctl unload ~/Library/LaunchAgents/com.br-to.news-radio.plist
launchctl load ~/Library/LaunchAgents/com.br-to.news-radio.plist
```

ログは `logs/daily.log` / `logs/daily.err.log` に出力される。

## ライセンス

MIT
