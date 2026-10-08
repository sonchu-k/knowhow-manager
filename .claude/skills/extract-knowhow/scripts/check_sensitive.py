#!/usr/bin/env python3
"""ノウハウファイルに特定情報が残っていないかを機械的に確認する。

使い方:
    python3 check_sensitive.py [--strict] [PATH ...]   PATH を確認(省略時は設定の knowhow_dir)
    python3 check_sensitive.py --pre-commit            コミット対象のファイルを確認(git フック用)
    python3 check_sensitive.py --show-config           解決済みのフォルダ設定を表示

フォルダの場所は knowhow.config.json で指定する。knowhow.config.local.json があれば
その値で上書きする。どちらもなければ既定値(knowhow / inbox / .sensitive-terms.txt)を使う。
相対パスは設定ファイルのあるフォルダが基準。絶対パスと ~ も使える。
抽象化の度合い(abstraction_level: low / medium / high)も同じファイルで指定する。

終了コード: 0 = 問題なし、1 = 特定情報の疑いあり、2 = 設定や引数の誤り。
--strict を付けると警告もエラーとして扱う。
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
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
    "敬称付きの名前": re.compile(r"[一-龥々]{1,4}(?:さん|様|氏)(?![名族々子式])"),
}

# 敬称パターンに一致するが人名ではない語(一致した文字列の末尾で判定する)
NOT_A_NAME_SUFFIXES = (
    "客様", "皆様", "皆さん", "奥様",
    "仕様", "同様", "模様", "多様", "一様", "異様", "両様", "各様",
    "彼氏", "某氏", "両氏", "各氏",
)

CONFIG_FILENAME = "knowhow.config.json"
LOCAL_CONFIG_FILENAME = "knowhow.config.local.json"
DEFAULTS = {
    "knowhow_dir": "knowhow",
    "inbox_dir": "inbox",
    "sensitive_terms_file": ".sensitive-terms.txt",
}


# パス以外の設定: キー -> (既定値, 使える値)
OPTIONS = {
    "abstraction_level": ("high", ("low", "medium", "high")),
}


class ConfigError(Exception):
    pass


def find_root(start: Path) -> Path:
    for directory in [start, *start.parents]:
        if (directory / CONFIG_FILENAME).is_file() or (directory / LOCAL_CONFIG_FILENAME).is_file():
            return directory
    return start


def load_config(
    config_path: Path | None,
) -> tuple[Path, list[Path], dict[str, Path], dict[str, str]]:
    """(基準フォルダ, 読み込んだ設定ファイル, 解決済みパス, パス以外の設定) を返す。"""
    if config_path is not None:
        if not config_path.is_file():
            raise ConfigError(f"設定ファイルが見つかりません: {config_path}")
        root = config_path.resolve().parent
        candidates = [config_path]
    else:
        root = find_root(Path.cwd().resolve())
        candidates = [root / CONFIG_FILENAME, root / LOCAL_CONFIG_FILENAME]

    values = {**DEFAULTS, **{key: default for key, (default, _) in OPTIONS.items()}}
    loaded = []
    for candidate in candidates:
        if not candidate.is_file():
            continue
        try:
            data = json.loads(candidate.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ConfigError(f"{candidate}: JSON として読めません({error})")
        if not isinstance(data, dict):
            raise ConfigError(f"{candidate}: オブジェクト形式で書いてください")
        unknown = sorted(set(data) - set(values))
        if unknown:
            raise ConfigError(
                f"{candidate}: 未知のキー {', '.join(unknown)}(使えるのは {', '.join(values)})"
            )
        for key, value in data.items():
            if not isinstance(value, str) or not value.strip():
                raise ConfigError(f"{candidate}: {key} は空でない文字列で指定してください")
        for key, (_, allowed) in OPTIONS.items():
            if key in data and data[key] not in allowed:
                raise ConfigError(
                    f"{candidate}: {key} は {' / '.join(allowed)} のいずれかで指定してください"
                )
        values.update(data)
        loaded.append(candidate)

    resolved = {}
    for key in DEFAULTS:
        path = Path(values[key]).expanduser()
        resolved[key] = (path if path.is_absolute() else root / path).resolve()
    return root, loaded, resolved, {key: values[key] for key in OPTIONS}


def load_terms(path: Path) -> list[str]:
    if not path.is_file():
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
        else:
            raise ConfigError(f"確認対象が見つかりません: {path}")
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
                if match.group().endswith(NOT_A_NAME_SUFFIXES):
                    continue
                warnings.append(f"{location}: [{label}] {match.group()}")
    return errors, warnings


def git(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, cwd=cwd)


def git_toplevel(directory: Path) -> Path | None:
    if not directory.is_dir():
        return None
    result = git("rev-parse", "--show-toplevel", cwd=directory)
    return Path(result.stdout.strip()).resolve() if result.returncode == 0 else None


def staged_files() -> list[Path]:
    toplevel = git_toplevel(Path.cwd())
    if toplevel is None:
        raise ConfigError("git リポジトリの中で実行してください")
    result = git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACM", cwd=toplevel)
    return [toplevel / name for name in result.stdout.split("\0") if name]


def show_config(
    root: Path, loaded: list[Path], paths: dict[str, Path], options: dict[str, str]
) -> int:
    print(f"基準フォルダ: {root}")
    names = ", ".join(path.name for path in loaded) or "なし(既定値を使用)"
    print(f"設定ファイル: {names}")
    for key, path in paths.items():
        note = "" if path.exists() else "  ※存在しません"
        print(f"{key}: {path}{note}")
    for key, value in options.items():
        print(f"{key}: {value}")

    inbox = paths["inbox_dir"]
    toplevel = git_toplevel(inbox)
    if toplevel is not None:
        probe = inbox / "probe.txt"
        if git("check-ignore", "-q", str(probe), cwd=toplevel).returncode != 0:
            print(
                f"WARNING inbox_dir が git 管理対象になっています。.gitignore に追加してください: {inbox}",
                file=sys.stderr,
            )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, help="確認するファイルやフォルダ(省略時は knowhow_dir)")
    parser.add_argument("--config", type=Path, help=f"設定ファイル(既定: {CONFIG_FILENAME} を上位へ探索)")
    parser.add_argument("--strict", action="store_true", help="警告もエラーとして扱う")
    parser.add_argument("--pre-commit", action="store_true", help="コミット対象のファイルを確認する")
    parser.add_argument("--show-config", action="store_true", help="解決済みのフォルダ設定を表示する")
    args = parser.parse_args()

    try:
        root, loaded, paths, options = load_config(args.config)
        if args.show_config:
            return show_config(root, loaded, paths, options)

        blocked = []
        if args.pre_commit:
            staged = [path.resolve() for path in staged_files()]
            blocked = [
                path
                for path in staged
                if path.is_relative_to(paths["inbox_dir"]) and path.name != ".gitkeep"
            ]
            files = [
                path
                for path in staged
                if path.suffix == ".md" and path.is_relative_to(paths["knowhow_dir"])
            ]
        else:
            files = collect_files(args.paths or [paths["knowhow_dir"]])
    except ConfigError as error:
        print(f"設定エラー: {error}", file=sys.stderr)
        return 2

    terms = load_terms(paths["sensitive_terms_file"])
    errors, warnings = [], []
    for path in blocked:
        errors.append(f"{path}: [元資料] inbox_dir 配下のファイルはコミットできません")
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
