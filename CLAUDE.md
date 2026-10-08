# knowhow-manager

A repository for extracting know-how from material with the identifying information removed, and accumulating it.

## Layout

- `knowhow.config.json` — folder locations and the abstraction level. `knowhow.config.local.json` (untracked by git) takes precedence when present
- `knowhow/` — accumulated know-how (default for `knowhow_dir`). `<category>/<title>.md`, indexed by `INDEX.md`
- `inbox/` — where unprocessed source documents are placed (default for `inbox_dir`). Untracked by git
- `policies/` — where confidentiality agreements and internal regulations are placed (default for `policies_dir`). Untracked by git
- `.claude/skills/extract-knowhow/` — skill that extracts know-how from material and saves it
- `.claude/skills/search-knowhow/` — skill that searches and references accumulated know-how
- `.claude/skills/check-policy/` — skill that judges the settings and practice against a policy
- `.sensitive-terms.txt` — list of proper nouns to detect (default for `sensitive_terms_file`). Untracked by git

## Rules

- Write the files in this repository (skills, references, scripts, README, commit messages) in English. Talk to the user, and write know-how, in the user's language.
- Do not hard-code where know-how or source documents live. Check `knowhow.config.json` and `knowhow.config.local.json` first.
- Follow the `extract-knowhow` skill when taking know-how out of material.
- How far to abstract follows `abstraction_level` in `knowhow.config.json` (`low` / `medium` / `high`, default `high`). If the request names a level, that takes precedence for that request only.
- At `high`, write a principle that holds when the setting changes, not a record of an event with the proper nouns removed. Do not carry over the source's item names, ordering, wording, or narrative.
- When the user's comment or instruction is the basis for the know-how, do not swap the claim for something else, and do not fill in unstated reasons or conditions by guessing.
- Do not save know-how until the full draft has been shown to the user and they have confirmed it is fine. If corrections come back, revise and show it again. Drafts go in `<inbox_dir>/_drafts/`.
- Follow the `search-knowhow` skill when looking up or referencing accumulated know-how. Keep what is in the store separate from general knowledge.
- Follow the `check-policy` skill when checking against a policy (confidentiality agreement, internal regulation, and so on). The judgment is groundwork, not a legal judgment. Never say "compliant" where there is doubt. Do not write policy text or the counterparty's name into any git-tracked file.
- Do not write source content or quotations into any git-tracked file. Keep proper nouns from the source out of commit messages too.
- After adding or changing know-how, run `python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py`.
- Commit or push only when the user asks.
