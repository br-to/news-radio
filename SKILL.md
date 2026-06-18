---
name: news-radio
description: "Collect news via web search, feed to NotebookLM, and generate Audio Overview podcast."
---

# News Radio

ニュースを収集し、NotebookLM CLI で Audio Overview（ポッドキャスト）を生成するスキル。

## 前提条件

- `notebooklm` CLI インストール済み・認証済み (`pip install notebooklm-py && notebooklm auth login`)
- ノートブック「News Radio」が作成済み (`notebooklm create "News Radio"` で作成し `notebooklm use <id>` でセット)

## ワークフロー

1. web_search でニュースを収集（5〜8件、blockchain/AI/prediction market 関連）
2. 収集結果をテキストにまとめて `/tmp/news_radio_input.txt` に保存
3. 既存ソースを削除: `notebooklm source delete <source_id>`
4. 新しいソースを追加: `notebooklm source add /tmp/news_radio_input.txt --title "Today's News"`
5. Audio Overview 生成: `notebooklm generate audio --length default --wait --timeout 900 --language ja --retry 2`
6. エラー時のみ通知

## ニュース収集テキストのフォーマット

```
# Today's News - YYYY-MM-DD

## 1. [タイトル]
[2-3行の要約]
URL: https://...

## 2. [タイトル]
...
```

## コマンドリファレンス

```bash
# ソース一覧
notebooklm source list

# ソース削除（IDで指定）
notebooklm source delete <source_id>

# ソース追加
notebooklm source add /tmp/news_radio_input.txt --title "Today's News"

# Audio Overview 生成
notebooklm generate audio --length default --wait --timeout 900 --language ja --retry 2

# 生成済みアーティファクト確認
notebooklm artifact list
```

## 注意事項

- NotebookLM Free は 3回/日、Plus は上限アップ
- 生成に 15-20 分かかる
- `--wait` を付けないと非同期実行（完了確認が別途必要）
- 既存ソースを消してから新しいのを追加すること（古いニュースが混ざる）
