# knowhow-manager

生成AIを使って、日々の資料からノウハウを蓄積していくためのリポジトリ。

議事録・提案書・チャットログ・振り返りメモなどを渡すと、企業情報や個人情報などの特定情報を取り除いたうえで、別の場面でも使える知見だけを抽出してノウハウフォルダ(既定では `knowhow/`)に保存する。蓄積したノウハウは、状況や質問を伝えると検索して提示される。

## 使い方

### Claude Code で使う

1. 初回のみ、コミット前チェックを有効にする。

   ```bash
   git config core.hooksPath .githooks
   cp .sensitive-terms.example.txt .sensitive-terms.txt   # 自社名・顧客名などを登録
   ```

2. 資料を元資料フォルダ(既定では `inbox/`、git 管理外)に置く。
3. このリポジトリで Claude Code を開き、依頼する。

   ```
   inbox/ の議事録からノウハウを抽出して
   ```

4. ノウハウフォルダに追加・更新された内容を確認してからコミットする。

蓄積したノウハウを使うときは、状況や質問をそのまま伝える。

   ```
   来週、初めての顧客に見積もりを出す。関係するノウハウある?
   ```

該当するノウハウが出典付きで提示され、蓄積がない観点は「該当なし」と明示される。

### チャット(claude.ai など)で使う

`.claude/skills/extract-knowhow/` と `.claude/skills/search-knowhow/` を、それぞれ zip にしてスキルとしてアップロードする。

- 抽出: ファイルを添付して「ノウハウを抽出して」と依頼すると、同じ書式のノウハウが回答として出力されるので、ノウハウフォルダに保存する。
- 検索: チャットからはノウハウフォルダを参照できないので、ノウハウファイルや `INDEX.md` を添付して質問する。

## フォルダの設定

ノウハウの保存先や元資料の置き場は `knowhow.config.json` で指定する。

```json
{
  "knowhow_dir": "knowhow",
  "inbox_dir": "inbox",
  "sensitive_terms_file": ".sensitive-terms.txt"
}
```

| キー | 意味 |
|---|---|
| `knowhow_dir` | ノウハウの保存先。目次の `INDEX.md` もここに置かれる |
| `inbox_dir` | 処理前の元資料の置き場 |
| `sensitive_terms_file` | 検出したい固有名詞のリスト |

- 相対パスは設定ファイルのあるフォルダが基準。絶対パスや `~` も使えるので、リポジトリの外(Obsidian の保管庫など)も指定できる。
- 自分の環境だけで変えたい場合は、同じ形式の `knowhow.config.local.json` を作る(git 管理外)。書いたキーだけが上書きされる。
- `inbox_dir` をリポジトリ内の別フォルダに変えたときは、`.gitignore` にもそのフォルダを追加する。
- `knowhow_dir` をリポジトリの外にすると、このリポジトリのコミット前フックは効かない。機械チェックは手動で実行する。

```bash
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py --show-config   # 解決後のパスを確認
```

## 構成

```
knowhow.config.json          フォルダの場所の設定
knowhow/                     蓄積されたノウハウ(<カテゴリ>/<タイトル>.md)
  INDEX.md                   目次
inbox/                       処理前の元資料(git 管理外)
.claude/skills/extract-knowhow/
  SKILL.md                   抽出の手順
  references/                特定情報の扱い、ノウハウの書式
  scripts/check_sensitive.py 特定情報の機械チェック
.claude/skills/search-knowhow/
  SKILL.md                   検索・参照の手順
.githooks/pre-commit         コミット時に機械チェックを実行
.sensitive-terms.example.txt 登録語リストの雛形
```

## 特定情報を残さないための仕組み

1. **スキルの手順**: 抽出前に特定情報を洗い出し、役割や性質に置き換えて書き、書いたあとに読み直す。
2. **機械チェック**: メールアドレス・電話番号・郵便番号・IPアドレス、および `.sensitive-terms.txt` に登録した語が含まれていればエラー。法人格・URL・敬称付きの名前は警告。
3. **コミット前フック**: ノウハウフォルダの変更に対して機械チェックを実行し、元資料フォルダのファイルのコミットを拒否する。

機械チェックで拾えるのは形式的なパターンと登録語だけで、文脈から特定できる記述(業界・地域・規模の組み合わせなど)は検出できない。コミット前に人の目でも確認すること。

```bash
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py            # ノウハウフォルダ全体
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py --strict   # 警告もエラー扱い
```
