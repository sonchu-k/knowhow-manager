#!/usr/bin/env python3
"""Mechanically check know-how files for leftover identifying information.

Usage:
    python3 check_sensitive.py [--strict] [PATH ...]   check PATH (default: the configured knowhow_dir)
    python3 check_sensitive.py --pre-commit            check the files staged for commit (for the git hook)
    python3 check_sensitive.py --show-config           show the resolved settings

Settings come from knowhow.config.json; values in knowhow.config.local.json override
them. With neither file, the defaults apply (knowhow / inbox / .sensitive-terms.txt /
policies). Relative paths are resolved from the folder holding the config file;
absolute paths and ~ also work. The abstraction level (abstraction_level: low /
medium / high) is set in the same file.

Exit codes: 0 = clean, 1 = possible identifying information, 2 = bad settings or arguments.
With --strict, warnings count as errors.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# The phone, postal code, corporate suffix and honorific patterns target Japanese text.
ERROR_PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "phone number": re.compile(
        r"(?<![\d-])0\d{1,4}-\d{1,4}-\d{3,4}(?![\d-])"
        r"|(?<!\d)0[789]0\d{8}(?!\d)"
        r"|\+81[\d-]{9,}"
    ),
    "postal code": re.compile(r"(?<![\d-])\d{3}-\d{4}(?![\d-])"),
    "IP address": re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
}

WARNING_PATTERNS = {
    "corporate suffix": re.compile(
        r"株式会社|有限会社|合同会社|㈱|\bInc\.|\bCo\.,? ?Ltd\b|\bLLC\b|\bCorp\."
    ),
    "URL": re.compile(r"https?://[^\s)>\]]+"),
    "name with honorific": re.compile(r"[一-龥々]{1,4}(?:さん|様|氏)(?![名族々子式])"),
}

# Words that match the honorific pattern but are not names (judged by the end of the match)
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
    "policies_dir": "policies",
}

# Folders whose contents must never go into git (source documents, policies)
PRIVATE_DIR_KEYS = ("inbox_dir", "policies_dir")

# Non-path settings: key -> (default, allowed values)
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
    """Return (base folder, config files read, resolved paths, non-path settings)."""
    if config_path is not None:
        if not config_path.is_file():
            raise ConfigError(f"config file not found: {config_path}")
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
            raise ConfigError(f"{candidate}: not valid JSON ({error})")
        if not isinstance(data, dict):
            raise ConfigError(f"{candidate}: must be a JSON object")
        unknown = sorted(set(data) - set(values))
        if unknown:
            raise ConfigError(
                f"{candidate}: unknown key(s) {', '.join(unknown)} (allowed: {', '.join(values)})"
            )
        for key, value in data.items():
            if not isinstance(value, str) or not value.strip():
                raise ConfigError(f"{candidate}: {key} must be a non-empty string")
        for key, (_, allowed) in OPTIONS.items():
            if key in data and data[key] not in allowed:
                raise ConfigError(f"{candidate}: {key} must be one of {' / '.join(allowed)}")
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
            raise ConfigError(f"nothing to check at: {path}")
    return files


def check_file(path: Path, terms: list[str]) -> tuple[list[str], list[str]]:
    errors, warnings = [], []
    lowered_terms = [(term, term.lower()) for term in terms]
    name_lower = path.name.lower()
    for term, lowered in lowered_terms:
        if lowered in name_lower:
            errors.append(f"{path}: [registered term] file name contains \"{term}\"")

    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        location = f"{path}:{number}"
        line_lower = line.lower()
        for term, lowered in lowered_terms:
            if lowered in line_lower:
                errors.append(f"{location}: [registered term] {term}")
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


def is_ignored(directory: Path) -> bool | None:
    """Whether git ignores the folder's contents. None if the folder is outside git."""
    toplevel = git_toplevel(directory)
    if toplevel is None:
        return None
    probe = directory / "probe.txt"
    return git("check-ignore", "-q", str(probe), cwd=toplevel).returncode == 0


def staged_files() -> list[Path]:
    toplevel = git_toplevel(Path.cwd())
    if toplevel is None:
        raise ConfigError("run this inside a git repository")
    result = git("diff", "--cached", "--name-only", "-z", "--diff-filter=ACM", cwd=toplevel)
    return [toplevel / name for name in result.stdout.split("\0") if name]


def show_config(
    root: Path, loaded: list[Path], paths: dict[str, Path], options: dict[str, str]
) -> int:
    print(f"base folder: {root}")
    names = ", ".join(path.name for path in loaded) or "none (using defaults)"
    print(f"config files: {names}")
    for key, path in paths.items():
        note = "" if path.exists() else "  (does not exist)"
        print(f"{key}: {path}{note}")
    for key, value in options.items():
        print(f"{key}: {value}")

    for key in PRIVATE_DIR_KEYS:
        if is_ignored(paths[key]) is False:
            print(
                f"WARNING {key} is tracked by git. Add it to .gitignore: {paths[key]}",
                file=sys.stderr,
            )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, help="files or folders to check (default: knowhow_dir)")
    parser.add_argument("--config", type=Path, help=f"config file (default: search upward for {CONFIG_FILENAME})")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--pre-commit", action="store_true", help="check the files staged for commit")
    parser.add_argument("--show-config", action="store_true", help="show the resolved settings")
    args = parser.parse_args()

    try:
        root, loaded, paths, options = load_config(args.config)
        if args.show_config:
            return show_config(root, loaded, paths, options)

        blocked = []
        if args.pre_commit:
            staged = [path.resolve() for path in staged_files()]
            blocked = [
                (key, path)
                for path in staged
                for key in PRIVATE_DIR_KEYS
                if path.is_relative_to(paths[key]) and path.name != ".gitkeep"
            ]
            files = [
                path
                for path in staged
                if path.suffix == ".md" and path.is_relative_to(paths["knowhow_dir"])
            ]
        else:
            files = collect_files(args.paths or [paths["knowhow_dir"]])
    except ConfigError as error:
        print(f"config error: {error}", file=sys.stderr)
        return 2

    terms = load_terms(paths["sensitive_terms_file"])
    errors, warnings = [], []
    for key, path in blocked:
        errors.append(f"{path}: [private] files under {key} cannot be committed")
    for path in files:
        file_errors, file_warnings = check_file(path, terms)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    for message in errors:
        print(f"ERROR   {message}")
    for message in warnings:
        print(f"WARNING {message}")

    print(
        f"Checked {len(files)} file(s): {len(errors)} error(s), {len(warnings)} warning(s)"
        f" ({len(terms)} registered term(s))",
        file=sys.stderr,
    )
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
