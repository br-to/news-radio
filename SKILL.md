---
name: news-radio
description: "Collect news via web search, feed to NotebookLM, and generate Audio Overview podcast."
---

# News Radio

ニュースを収集し、NotebookLM で Audio Overview（ポッドキャスト）を生成するスキル。

## 前提条件

- `notebooklm` CLI インストール済み・認証済み (`pip install notebooklm-py && notebooklm auth login`)
- ノートブック「News Radio」が作成済み (`notebooklm create "News Radio"` で作成し `notebooklm use <id>` でセット)
- `news-radio` パッケージがインストール済み (`pip install -e .`)

## Cowork 向けワークフロー（推奨）

Cowork は長時間の `--wait` に向いていない。**ニュース収集だけ Cowork に任せ、音声生成は 1 コマンドで非同期キック**する。

1. web_search でニュースを収集（5〜8件、blockchain/AI/prediction market 関連）
2. 収集結果をテキストにまとめて `/tmp/news_radio_input.txt` に保存
3. **1 コマンドで生成開始（非同期）**:
   ```bash
   python -m news_radio --async /tmp/news_radio_input.txt
   ```
4. 完了は NotebookLM アプリのプッシュ通知で確認（15〜20 分後）

### Cowork でうまくいかない典型パターン

| 問題 | 原因 | 対策 |
|------|------|------|
| 途中で止まる | `--wait` で 15〜20 分ブロック | `--async` を使う |
| CLI 手順が多すぎる | source delete/add を個別実行 | `python -m news_radio` に集約 |
| 認証エラー | Cowork 実行環境に notebooklm 認証がない | **notebooklm 認証済みのマシン**で実行する |

## ローカル実行（MP3 ダウンロードまで待つ）

```bash
python -m news_radio /tmp/news_radio_input.txt
# または
echo "Today's news..." | python -m news_radio
```

## ニュース収集テキストのフォーマット

```
# Today's News - YYYY-MM-DD

## 1. [タイトル]
[2-3行の要約]
URL: https://...

## 2. [タイトル]
...
```

## 代替案（Cowork を使わない）

### A. cron + ローカルスクリプト（最も安定）

notebooklm 認証済みのマシンで毎朝 cron 実行。ニュース収集は別途（手動 or 別エージェント）。

```bash
# crontab 例: 毎朝 7:00
0 7 * * * /path/to/news-radio/scripts/daily.sh
```

### B. Cursor Cloud Agent / Automation

リポジトリを指定して定期実行。Private Worker を使えば notebooklm 認証済みローカル環境で動かせる。

### C. 2 段階に分離

1. Cowork: ニュース収集 → テキストファイルを GDrive/Dropbox に保存
2. ローカル: ファイル同期後に `python -m news_radio --async` を実行

## コマンドリファレンス

```bash
# 非同期（Cowork / 自動化向け）
python -m news_radio --async /tmp/news_radio_input.txt

# 同期（MP3 ダウンロードまで待つ）
python -m news_radio /tmp/news_radio_input.txt

# 生成済みアーティファクト確認
notebooklm artifact list
```

## 注意事項

- NotebookLM Free は 3回/日、Plus は上限アップ
- 生成に 15-20 分かかる
- `--async` では MP3 ダウンロードは行わない（NotebookLM アプリで聴く）
