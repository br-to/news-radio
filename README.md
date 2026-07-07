# News Radio

毎朝のニュースを NotebookLM の Audio Overview 機能でラジオ風音声に変換し、Discord に投稿するツール。

## アーキテクチャ

```
[Mac / PC の cron]  毎朝 7:00
       |
       v
[Brave Search API] --- AI / blockchain / prediction market のニュース収集
       |
       v
[notebooklm CLI] --- Audio Overview (default length) を生成
       |
       v
[Discord Webhook] --- MP3 を投稿 + 進捗・エラー通知
```

## 技術スタック

- Python 3.12
- [notebooklm CLI](https://github.com/teng-lin/notebooklm-py) - NotebookLM CLI クライアント
- Brave Search API - ニュース検索
- Discord Webhook - 音声配信・通知

## セットアップ

```bash
git clone https://github.com/br-to/news-radio.git
cd news-radio
pip install -e .
cp .env.example .env  # API キーを設定
```

### 環境変数

| 変数名 | 必須 | 説明 |
|--------|------|------|
| `BRAVE_API_KEY` | 自動モード時 | [Brave Search API](https://api.search.brave.com) キー |
| `DISCORD_WEBHOOK_URL` | 推奨 | Discord Webhook URL |
| `NEWS_QUERIES` | 任意 | 検索クエリ（カンマ区切り） |

### notebooklm CLI 認証

```bash
pip install notebooklm-py
notebooklm auth login
notebooklm create "News Radio" --json
notebooklm use <notebook_id>
```

## 使い方

```bash
# 完全自動（Brave Search → 音声生成 → Discord 投稿）
python -m news_radio

# ファイルから（Discord 投稿あり）
python -m news_radio news.txt

# 非同期（生成キックのみ、Discord には開始通知）
python -m news_radio --async news.txt
```

## 完全自動化（OpenClaw 不要）

**動かす場所 = 普段使ってる Mac / PC 本体。** OpenClaw も Cowork も不要。

notebooklm のログイン状態はそのマシンに保存されるので、cron も同じマシンで回す。

### Mac（おすすめ）

```bash
# 1. セットアップ
git clone https://github.com/br-to/news-radio.git
cd news-radio
pip install -e .
cp .env.example .env          # キーを埋める
notebooklm auth login         # ブラウザで Google ログイン
notebooklm use <notebook_id>

# 2. 動作確認
./scripts/daily.sh

# 3. 毎朝 7:00 に自動実行（launchd）
chmod +x scripts/install-macos.sh
./scripts/install-macos.sh
```

Mac が 7 時にスリープしてると動かない。  
「システム設定 → バッテリー → スケジュール」で 6:55 に起動、などの設定が必要。

### Linux / WSL

```bash
crontab -e
# 毎朝 7:00
0 7 * * * /path/to/news-radio/scripts/daily.sh >> /tmp/news-radio.log 2>&1
```

### 常時起動マシンがない場合

| 方法 | 内容 |
|------|------|
| 古い PC / Raspberry Pi | 安価な常時起動マシンにセットアップ |
| 手動実行 | 朝 `./scripts/daily.sh` を叩く（Discord 通知は来る） |
| Cursor Automation | Private Worker 経由でローカル実行（Cursor 契約者向け） |

## 音声スタイル

プロンプト指示で落ち着いたトーンで生成。大袈裟なリアクションを抑えた淡々としたニュース解説形式。

## ライセンス

MIT
