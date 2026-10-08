#!/usr/bin/env python3
"""Gather the current settings and storage state for a policy check.

Usage:
    python3 policy_facts.py [--config FILE]

Never prints file contents or the registered terms themselves; only counts and locations.
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
    print("scripts/check_sensitive.py of the extract-knowhow skill was not found.", file=sys.stderr)
    sys.exit(2)

# If one of these appears in a path, the folder is probably synced to a cloud service
SYNC_MARKERS = ("Mobile Documents", "CloudStorage", "iCloud", "Dropbox", "OneDrive", "Google Drive", "GoogleDrive", "Box Sync")

ABSTRACTION_LINE = re.compile(r"^abstraction:\s*(\S+)", re.MULTILINE)


def yes_no(value: bool | None) -> str:
    return "unknown" if value is None else ("yes" if value else "no")


def describe_location(label: str, path: Path) -> None:
    print(f"[{label}] {path}")
    print(f"  exists: {yes_no(path.exists())}")
    toplevel = cs.git_toplevel(path if path.is_dir() else path.parent)
    if toplevel is None:
        print("  inside a git repository: no")
    else:
        print(f"  inside a git repository: yes ({toplevel})")
        if path.is_dir():
            print(f"  contents ignored by git: {yes_no(cs.is_ignored(path))}")
        remotes = cs.git("remote", "-v", cwd=toplevel).stdout.split("\n")
        urls = sorted({line.split()[1] for line in remotes if len(line.split()) >= 2})
        print(f"  remotes: {', '.join(urls) if urls else 'none'}")
    marker = next((m for m in SYNC_MARKERS if m in str(path)), None)
    print(f"  looks like a cloud-synced folder: {'yes (' + marker + ')' if marker else 'not apparent from the path'}")


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
        print(f"config error: {error}", file=sys.stderr)
        return 2

    print("== Settings ==")
    print(f"base folder: {root}")
    print(f"config files: {', '.join(p.name for p in loaded) or 'none (using defaults)'}")
    for key, value in options.items():
        print(f"{key}: {value}")

    print("\n== Storage ==")
    describe_location("know-how: knowhow_dir", paths["knowhow_dir"])
    describe_location("source documents: inbox_dir", paths["inbox_dir"])
    describe_location("policies: policies_dir", paths["policies_dir"])

    print("\n== What is stored ==")
    knowhow = paths["knowhow_dir"]
    levels: dict[str, int] = {}
    if knowhow.is_dir():
        for path in knowhow.rglob("*.md"):
            if path.name == "INDEX.md":
                continue
            match = ABSTRACTION_LINE.search(path.read_text(encoding="utf-8"))
            level = match.group(1) if match else "not recorded"
            levels[level] = levels.get(level, 0) + 1
    total = sum(levels.values())
    detail = ", ".join(f"{k}: {v}" for k, v in sorted(levels.items())) or "none"
    print(f"saved know-how: {total} (by abstraction level: {detail})")
    inbox = paths["inbox_dir"]
    drafts = count_files(inbox / "_drafts")
    print(f"files left in the inbox folder: {count_files(inbox) - drafts}")
    print(f"drafts awaiting confirmation: {drafts}")
    print(f"files in the policy folder: {count_files(paths['policies_dir'])}")

    print("\n== Safeguards ==")
    terms = paths["sensitive_terms_file"]
    print(f"terms file: {'present (' + str(len(cs.load_terms(terms))) + ' term(s))' if terms.is_file() else 'absent'}")
    toplevel = cs.git_toplevel(root)
    if toplevel is None:
        print("pre-commit hook: not applicable (the base folder is not a git repository)")
    else:
        hooks = cs.git("config", "core.hooksPath", cwd=toplevel).stdout.strip()
        enabled = hooks == ".githooks" and (toplevel / ".githooks" / "pre-commit").is_file()
        print(f"pre-commit hook: {'enabled' if enabled else 'disabled (enable with: git config core.hooksPath .githooks)'}")

    print("\n== Not knowable from here (ask the user) ==")
    print("- The generative-AI service's contract type and holder (personal, or which organization's), and how inputs are handled (use for training, retention period, storage region)")
    print("- The status of procedures the policy requires (prior consent, notification, usage records)")
    print("- The visibility of the remote repository and who can access it")
    print("- Whether this device or folder is shared with anyone else")
    return 0


if __name__ == "__main__":
    sys.exit(main())
