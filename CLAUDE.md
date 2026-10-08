# knowhow-manager

資料から特定情報を除いたノウハウを抽出し、蓄積するリポジトリ。

## 構成

- `knowhow.config.json` — フォルダの場所の設定。`knowhow.config.local.json`(git 管理外)があればそちらが優先
- `knowhow/` — 蓄積されたノウハウ(`knowhow_dir` の既定値)。`<カテゴリ>/<タイトル>.md`、目次は `INDEX.md`
- `inbox/` — 処理前の元資料を置く場所(`inbox_dir` の既定値)。git 管理外
- `.claude/skills/extract-knowhow/` — 資料からノウハウを抽出・保存するスキル
- `.claude/skills/search-knowhow/` — 蓄積されたノウハウを検索・参照するスキル
- `.sensitive-terms.txt` — 検出したい固有名詞のリスト(`sensitive_terms_file` の既定値)。git 管理外

## ルール

- ノウハウや元資料の場所を決め打ちしない。作業の最初に `knowhow.config.json` と `knowhow.config.local.json` を確認する。
- 資料からノウハウを取り出す作業は `extract-knowhow` スキルの手順に従う。
- ノウハウは、下書きの全文をユーザーに見せて「問題ない」と確認が取れるまで保存しない。修正の指摘があれば直して見せ直す。下書きは `<inbox_dir>/_drafts/` に置く。
- 蓄積されたノウハウを調べる・参照する作業は `search-knowhow` スキルの手順に従う。蓄積にある内容と一般知識は分けて答える。
- 元資料の内容や引用を、git 管理対象のファイルに書かない。コミットメッセージにも元資料の固有名詞を書かない。
- ノウハウを追加・変更したら `python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py` を実行する。
- コミット・プッシュはユーザーに頼まれたときだけ行う。
