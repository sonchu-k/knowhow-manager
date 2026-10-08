# knowhow-manager

生成AIを使って、日々の資料からノウハウを蓄積していくためのリポジトリ。

議事録・提案書・チャットログ・振り返りメモなどを渡すと、企業情報や個人情報などの特定情報を取り除いたうえで、別の場面でも使える知見だけを抽出して `knowhow/` に保存する。

## 使い方

### Claude Code で使う

1. 初回のみ、コミット前チェックを有効にする。

   ```bash
   git config core.hooksPath .githooks
   cp .sensitive-terms.example.txt .sensitive-terms.txt   # 自社名・顧客名などを登録
   ```

2. 資料を `inbox/` に置く(このフォルダは git 管理外)。
3. このリポジトリで Claude Code を開き、依頼する。

   ```
   inbox/ の議事録からノウハウを抽出して
   ```

4. `knowhow/` に追加・更新された内容を確認してからコミットする。

### チャット(claude.ai など)で使う

`.claude/skills/extract-knowhow/` フォルダを zip にしてスキルとしてアップロードする。ファイルを添付して「ノウハウを抽出して」と依頼すると、同じ書式のノウハウが回答として出力されるので、`knowhow/` に保存する。

## 構成

```
knowhow/                     蓄積されたノウハウ(<カテゴリ>/<タイトル>.md)
  INDEX.md                   目次
inbox/                       処理前の元資料(git 管理外)
.claude/skills/extract-knowhow/
  SKILL.md                   抽出の手順
  references/                特定情報の扱い、ノウハウの書式
  scripts/check_sensitive.py 特定情報の機械チェック
.githooks/pre-commit         コミット時に機械チェックを実行
.sensitive-terms.example.txt 登録語リストの雛形
```

## 特定情報を残さないための仕組み

1. **スキルの手順**: 抽出前に特定情報を洗い出し、役割や性質に置き換えて書き、書いたあとに読み直す。
2. **機械チェック**: メールアドレス・電話番号・郵便番号・IPアドレス、および `.sensitive-terms.txt` に登録した語が含まれていればエラー。法人格・URL・敬称付きの名前は警告。
3. **コミット前フック**: `knowhow/` の変更に対して機械チェックを実行し、`inbox/` のファイルのコミットを拒否する。

機械チェックで拾えるのは形式的なパターンと登録語だけで、文脈から特定できる記述(業界・地域・規模の組み合わせなど)は検出できない。コミット前に人の目でも確認すること。

```bash
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py            # knowhow/ 全体
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py --strict   # 警告もエラー扱い
```
