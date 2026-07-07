---
name: news-radio
description: "Cowork workflow: web_search news → NotebookLM audio → Discord."
---

# News Radio（Cowork 版）

Cowork で完結させるニュースラジオ生成スキル。

## 前提条件

- `notebooklm` CLI インストール済み・認証済み（`notebooklm auth login`）
- ノートブック「News Radio」作成済み（`notebooklm use <id>`）
- `news-radio` インストール済み（`pip install -e .`）
- 環境変数 `DISCORD_WEBHOOK_URL` 設定済み

## Cowork ワークフロー（これだけ）

### Step 1: ニュース収集（web_search）

web_search で 5〜8 件集める。テーマ:

- AI / artificial intelligence
- blockchain / crypto
- prediction market

### Step 2: テキスト整形 → 保存

`/tmp/news_radio_input.txt` に以下フォーマットで保存:

```
# Today's News - YYYY-MM-DD

## 1. [タイトル]
[2-3行の要約]
URL: https://...

## 2. [タイトル]
...
```

### Step 3: 音声生成 + Discord 投稿（1コマンド）

```bash
python3 -m news_radio /tmp/news_radio_input.txt
```

これだけ。内部で source 差し替え → NotebookLM 生成 → Discord に MP3 投稿まで全部やる。

**15〜20 分かかる。Cowork セッションが切れる場合は非同期版:**

```bash
python3 -m news_radio --async /tmp/news_radio_input.txt
```

→ Discord に「生成開始」通知。MP3 は NotebookLM アプリの通知で確認。

---

## Cowork への指示例（コピペ用）

```
news-radio スキルを実行して。

1. web_search で AI / blockchain / prediction market の最新ニュースを 5〜8 件収集
2. /tmp/news_radio_input.txt に整形して保存
3. python3 -m news_radio /tmp/news_radio_input.txt を実行
4. 完了したら Discord に MP3 が届くはず。エラーなら内容を報告
```

---

## 環境変数

| 変数 | 必須 | 説明 |
|------|------|------|
| `DISCORD_WEBHOOK_URL` | ✅ | Discord Webhook URL |
| `BRAVE_API_KEY` | ❌ | Cowork では web_search を使うので不要 |

---

## Discord 通知

| タイミング | 内容 |
|-----------|------|
| 開始 | 📻 音声生成中 |
| 成功 | 🎙️ MP3 ファイル投稿 |
| 失敗 | ❌ エラーメッセージ |

---

## トラブルシュート

| 症状 | 対策 |
|------|------|
| Cowork が途中で止まる | `--async` 版を使う |
| notebooklm 認証エラー | Cowork 実行環境で `notebooklm auth login` |
| Discord に何も来ない | `DISCORD_WEBHOOK_URL` を確認 |
| 古いニュースが混ざる | 心配不要（実行時に既存ソースは自動削除される） |

---

## 代替: Brave Search 自動収集（Cowork 不要）

Cowork を使わず API で全部やる場合:

```bash
python3 -m news_radio   # BRAVE_API_KEY 必要
```

Mac cron / `--wake` 向け。Cowork 版では使わない。
