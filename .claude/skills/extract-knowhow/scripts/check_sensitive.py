#!/usr/bin/env python3
"""ノウハウファイルに特定情報が残っていないかを機械的に確認する。

使い方:
    python3 check_sensitive.py [--strict] [--terms FILE] [PATH ...]

PATH を省略すると knowhow/ を対象にする。エラーが1件でもあれば終了コード1。
--strict を付けると警告もエラーとして扱う。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ERROR_PATTERNS = {
    "メールアドレス": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "電話番号": re.compile(
        r"(?<![\d-])0\d{1,4}-\d{1,4}-\d{3,4}(?![\d-])"
        r"|(?<!\d)0[789]0\d{8}(?!\d)"
        r"|\+81[\d-]{9,}"
    ),
    "郵便番号": re.compile(r"(?<![\d-])\d{3}-\d{4}(?![\d-])"),
    "IPアドレス": re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
}

WARNING_PATTERNS = {
    "法人格": re.compile(
        r"株式会社|有限会社|合同会社|㈱|\bInc\.|\bCo\.,? ?Ltd\b|\bLLC\b|\bCorp\."
    ),
    "URL": re.compile(r"https?://[^\s)>\]]+"),
    "敬称付きの名前": re.compile(r"[一-龥々]{1,4}(?:さん|様|氏)(?![名族])"),
}

# 敬称パターンに一致するが人名ではない語
HONORIFIC_ALLOWLIST = {"客様", "皆様", "皆さん", "奥様", "各位様"}

TERMS_FILENAME = ".sensitive-terms.txt"


def find_terms_file(start: Path) -> Path | None:
    for directory in [start, *start.parents]:
        candidate = directory / TERMS_FILENAME
        if candidate.is_file():
            return candidate
    return None


def load_terms(path: Path | None) -> list[str]:
    if path is None:
        return []
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            terms.append(line)
    return terms


def collect_files(paths: list[Path]) -> list[Path]:
    files = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            files.append(path)
    return files


def check_file(path: Path, terms: list[str]) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    lowered_terms = [(term, term.lower()) for term in terms]
    name_lower = path.name.lower()
    for term, lowered in lowered_terms:
        if lowered in name_lower:
            errors.append(f"{path}: [登録語] ファイル名に「{term}」")

    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        location = f"{path}:{number}"
        line_lower = line.lower()
        for term, lowered in lowered_terms:
            if lowered in line_lower:
                errors.append(f"{location}: [登録語] {term}")
        for label, pattern in ERROR_PATTERNS.items():
            for match in pattern.finditer(line):
                errors.append(f"{location}: [{label}] {match.group()}")
        for label, pattern in WARNING_PATTERNS.items():
            for match in pattern.finditer(line):
                if match.group() in HONORIFIC_ALLOWLIST:
                    continue
                warnings.append(f"{location}: [{label}] {match.group()}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, default=[Path("knowhow")])
    parser.add_argument("--terms", type=Path, help=f"登録語ファイル(既定: {TERMS_FILENAME} を上位へ探索)")
    parser.add_argument("--strict", action="store_true", help="警告もエラーとして扱う")
    args = parser.parse_args()

    terms_file = args.terms or find_terms_file(Path.cwd())
    terms = load_terms(terms_file)
    files = collect_files(args.paths)

    errors, warnings = [], []
    for path in files:
        file_errors, file_warnings = check_file(path, terms)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    for message in errors:
        print(f"ERROR   {message}")
    for message in warnings:
        print(f"WARNING {message}")

    print(
        f"{len(files)} ファイルを確認: エラー {len(errors)} 件、警告 {len(warnings)} 件"
        f"(登録語 {len(terms)} 語)",
        file=sys.stderr,
    )
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
