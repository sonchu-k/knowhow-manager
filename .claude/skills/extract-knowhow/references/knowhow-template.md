# Know-how file format

Location: `<know-how folder>/<category>/<short title>.md` (the know-how folder is `knowhow_dir` in `knowhow.config.json`)

One know-how = one principle = one file.

```markdown
---
title: When you want a decision, lay out options to change the kind of decision
category: Proposals and agreement
tags: [agreement, options, presentation]
source_type: [document]
basis: result
abstraction: high
created: 2026-10-08
updated: 2026-10-08
evidence_count: 1
---

# When you want a decision, lay out options to change the kind of decision

## Key point

With one option the other party's decision is "accept or refuse"; with several it becomes "which one". When you want a decision, present things in a form that changes the kind of decision.

## Principle

Why it happens. The mechanism that holds when the setting changes, written without leaning on field vocabulary.

## When to use

Settings where the principle operates. Name several, not limited to the field of the source.

## How

Concrete actions for using the principle. A bullet list is fine.

## When it does not apply

Conditions under which it does not hold, cases where it backfires, unconfirmed points.

## Evidence

Kind and count only. Example: "One case where it was done and the result was confirmed." Do not narrate what happened.
```

## Language

Write the title, category, tags, and body in the user's language, including the section headings. In Japanese, use these headings so that files stay consistent: 要点 / 原理 / 使いどころ / やり方 / 当てはまらない場合 / 裏付け. Frontmatter keys and the fixed values of `source_type`, `basis`, and `abstraction` stay in English.

## Fields

- `title`: Make the principle, or the action based on it, clear. At `high`, do not lean on the source's field vocabulary ("When you want a decision, lay out options to change the kind of decision", not "Present three quotes"). At `medium` and `low`, field vocabulary is fine.
- `category`: Must match a folder name directly under the know-how folder. Divide by "what setting it is used in", not by the industry or kind of engagement of the source.
- `tags`: Words for the principle or the setting where it is used. Do not put back the industry, role, or kind of engagement removed from the body.
- `source_type`: A list chosen from the three values below. Do not write a finer type (tech blog, committee minutes).
  - `document`: articles, reports, proposals, notes
  - `meeting-or-conversation`: minutes, chat logs
  - `own-comment`: what the user said themselves
  - For both a document and a comment, write `[document, own-comment]`.
- `basis`: Kind of evidence. One of `result` (done and the result confirmed), `opinion` (based on views or impressions; result not confirmed), `rule-of-thumb` (based on the person's experience; reason and conditions not worked out).
- `abstraction`: The abstraction level this know-how was written at (`low` / `medium` / `high`). Use `abstraction_level` from the config, or the value named in the request.
- `evidence_count`: The number of **mutually independent documents or occasions** that support this know-how. One document or one comment counts as one however many cases it contains. Increase it when the same principle is confirmed by a different document or on a different occasion.
- "Key point" and "Principle" are required. If the principle is not known (a user comment with no reason given, for example), do not fill it by guessing; write "principle not confirmed (rule of thumb)".
- "When to use", "How", and "When it does not apply" may be omitted when there is nothing to write. If nothing at all can be written under "When it does not apply", suspect that it has gone up into a platitude.

The example above is written at `high`. At `low` and `medium`, "Principle" can be a short statement of the reason, and "How" carries the concrete steps and items in more detail. Keep the same headings at every level.

For the thinking behind this and the differences between levels, see [conceptualization.md](conceptualization.md).

## Adding to INDEX.md

Add one line under the category heading. Write the link relative to `INDEX.md`. If the path contains spaces, wrap it in angle brackets.

```markdown
## Proposals and agreement

- [When you want a decision, lay out options to change the kind of decision](<Proposals and agreement/When you want a decision, lay out options to change the kind of decision.md>) — one option makes it "accept or refuse"; several make it "which one"
```
