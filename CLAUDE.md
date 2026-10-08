# knowhow-manager

資料から特定情報を除いたノウハウを抽出し、蓄積するリポジトリ。

## 構成

- `knowhow/` — 蓄積されたノウハウ。`<カテゴリ>/<タイトル>.md`、目次は `knowhow/INDEX.md`
- `inbox/` — 処理前の元資料を置く場所。git 管理外
- `.claude/skills/extract-knowhow/` — 抽出スキル本体
- `.sensitive-terms.txt` — 検出したい固有名詞のリスト。git 管理外

## ルール

- 資料からノウハウを取り出す作業は `extract-knowhow` スキルの手順に従う。
- 元資料の内容や引用を、git 管理対象のファイルに書かない。コミットメッセージにも元資料の固有名詞を書かない。
- `knowhow/` を変更したら `python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py` を実行する。
- コミット・プッシュはユーザーに頼まれたときだけ行う。
