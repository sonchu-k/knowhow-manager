#!/usr/bin/env python3
"""規定チェックのために、現在の設定と保管の状況を集めて表示する。

使い方:
    python3 policy_facts.py [--config FILE]

ファイルの中身や登録語そのものは表示しない。件数と場所だけを出す。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "extract-knowhow" / "scripts"))
try:
    import check_sensitive as cs
except ImportError:
    print("extract-knowhow スキルの scripts/check_sensitive.py が見つかりません。", file=sys.stderr)
    sys.exit(2)

# パスに含まれていたら、クラウドと同期されている可能性が高い語
SYNC_MARKERS = ("Mobile Documents", "CloudStorage", "iCloud", "Dropbox", "OneDrive", "Google Drive", "GoogleDrive", "Box Sync")

ABSTRACTION_LINE = re.compile(r"^abstraction:\s*(\S+)", re.MULTILINE)


def yes_no(value: bool | None, unknown: str = "不明") -> str:
    return unknown if value is None else ("はい" if value else "いいえ")


def describe_location(label: str, path: Path) -> None:
    print(f"[{label}] {path}")
    print(f"  存在する: {yes_no(path.exists())}")
    toplevel = cs.git_toplevel(path if path.is_dir() else path.parent)
    if toplevel is None:
        print("  git リポジトリの中: いいえ")
    else:
        print(f"  git リポジトリの中: はい({toplevel})")
        if path.is_dir():
            print(f"  中身は git から無視される: {yes_no(cs.is_ignored(path))}")
        remotes = cs.git("remote", "-v", cwd=toplevel).stdout.split("\n")
        urls = sorted({line.split()[1] for line in remotes if len(line.split()) >= 2})
        print(f"  リモート: {', '.join(urls) if urls else 'なし'}")
    marker = next((m for m in SYNC_MARKERS if m in str(path)), None)
    print(f"  クラウド同期フォルダらしい場所: {'はい(' + marker + ')' if marker else 'パスからは見当たらない'}")


def count_files(directory: Path, pattern: str = "*") -> int:
    if not directory.is_dir():
        return 0
    return sum(1 for p in directory.rglob(pattern) if p.is_file() and p.name != ".gitkeep")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()
    try:
        root, loaded, paths, options = cs.load_config(args.config)
    except cs.ConfigError as error:
        print(f"設定エラー: {error}", file=sys.stderr)
        return 2

    print("== 設定 ==")
    print(f"基準フォルダ: {root}")
    print(f"設定ファイル: {', '.join(p.name for p in loaded) or 'なし(既定値を使用)'}")
    for key, value in options.items():
        print(f"{key}: {value}")

    print("\n== 保管場所 ==")
    describe_location("ノウハウ knowhow_dir", paths["knowhow_dir"])
    describe_location("元資料 inbox_dir", paths["inbox_dir"])
    describe_location("規定 policies_dir", paths["policies_dir"])

    print("\n== 蓄積の状況 ==")
    knowhow = paths["knowhow_dir"]
    levels: dict[str, int] = {}
    if knowhow.is_dir():
        for path in knowhow.rglob("*.md"):
            if path.name == "INDEX.md":
                continue
            match = ABSTRACTION_LINE.search(path.read_text(encoding="utf-8"))
            level = match.group(1) if match else "記録なし"
            levels[level] = levels.get(level, 0) + 1
    total = sum(levels.values())
    detail = "、".join(f"{k}: {v}" for k, v in sorted(levels.items())) or "なし"
    print(f"保存済みのノウハウ: {total} 件(抽象化の度合い別 — {detail})")
    inbox = paths["inbox_dir"]
    drafts = count_files(inbox / "_drafts")
    print(f"元資料フォルダに残っているファイル: {count_files(inbox) - drafts} 件")
    print(f"確認待ちの下書き: {drafts} 件")
    print(f"規定フォルダのファイル: {count_files(paths['policies_dir'])} 件")

    print("\n== 漏れを防ぐ仕組み ==")
    terms = paths["sensitive_terms_file"]
    print(f"登録語ファイル: {'あり(' + str(len(cs.load_terms(terms))) + ' 語)' if terms.is_file() else 'なし'}")
    toplevel = cs.git_toplevel(root)
    if toplevel is None:
        print("コミット前フック: 対象外(基準フォルダが git リポジトリではない)")
    else:
        hooks = cs.git("config", "core.hooksPath", cwd=toplevel).stdout.strip()
        enabled = hooks == ".githooks" and (toplevel / ".githooks" / "pre-commit").is_file()
        print(f"コミット前フック: {'有効' if enabled else '無効(git config core.hooksPath .githooks で有効化)'}")

    print("\n== ここからは分からないこと(ユーザーに確認する) ==")
    print("- 生成AIサービスの契約形態と名義(個人か、どの組織の契約か)、入力データの扱い(学習への利用、保存期間、保存される地域)")
    print("- 規定が求める手続きの状況(事前の承諾、届け出、利用の記録など)")
    print("- リモートリポジトリの公開範囲と、アクセスできる人")
    print("- この端末やフォルダを、ほかの人と共有しているか")
    return 0


if __name__ == "__main__":
    sys.exit(main())
