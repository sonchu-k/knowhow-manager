---
name: extract-knowhow
description: Extract reusable know-how from files or pasted text (meeting minutes, proposals, chat logs, retrospectives, emails, and the like). Removes identifying information such as company and personal details, lifts events up to principles that hold in other settings, shows the full draft to the user, and saves it only after they confirm. Also turns the user's own comments, experience, or instructions into know-how when there is no source document. Use when the user says things like "extract know-how from this", "capture the lessons from this document", "save this as know-how", "turn what I just said into know-how" (in Japanese, 「ノウハウを抽出して」「この資料から学びを残して」「これをノウハウとして残して」「ナレッジ化して」), or hands over material and asks to organize what was learned.
---

# Extract know-how

Take what was learned from a source document or from the user's comments and keep it as a **principle** that holds in other settings, written so that nobody can tell whose story or which company it came from. The goal is a principle, not a record of what happened.

Two things must both be true for the result to count as a success.

- **Reusable**: someone who has never seen the source can read it, apply it to their own situation, and act differently.
- **Not identifiable**: a reader cannot work out the company, person, or engagement behind it.

Removing proper nouns achieves neither. If the shape of the event survives, the result is hard to use in another field, and its structure and wording still give the source away. The approach is to **take the principle (why it happens) out of the event and rewrite it in your own words and structure**. That erases the shape of the source and makes the result usable elsewhere at the same time. Go too far up, though, and you get a platitude like "communication matters", something with no case where it fails to hold.

## Language

Work in the user's language. Talk to the user and write the know-how in the language they use. Frontmatter keys and the fixed values listed in the template (`basis`, `source_type`, `abstraction`) stay in English so that search and tooling keep working.

## What the know-how is based on

There are three cases. Work out which one applies first.

| Case | Example | What decides the content |
|---|---|---|
| Extract from a document | "Extract know-how from these minutes" | What the document says |
| Based on the user's comment | "Save this as know-how: always present three quotes. With one quote…" / "Turn that last point into know-how" | What the user said |
| A document with the user's comment attached | "The real lesson in this retrospective is that we never visited the site. Keep that." / "Only extract the points about price negotiation" | What the user said. The document is supporting evidence and detail |

When the user's comment is the basis, **the claim belongs to the user, and your job is to organize it and give it form**.

- **Do not swap the claim.** Do not replace what the user said with something you find more reasonable, or with a safe generality. Tidy the wording, but keep what to do and why.
- **Do not invent the missing parts.** If the user gave no reason or conditions, do not fill them in with something plausible. Write "reason not confirmed" in the draft and ask at confirmation. If you want to add something of your own, present it as a clearly marked suggestion and let the user decide.
- **Ask first only if the core is unclear.** If you cannot tell what the user is saying should be done, check briefly before drafting. Smaller gaps can wait until you show the draft.
- **Follow a stated scope.** If the user says "from this angle" or "only this", stay inside it. If the document holds other useful points, do not draft them; at confirmation, ask whether to keep them.
- **Do not hide a mismatch with the document.** If the user's reading and the document disagree, still write the know-how from the user's claim, and say at confirmation that they disagree.
- **Identifying information is handled the same way.** The user's comments contain names too. Remove them by the same standard as for documents, including when the basis is a correction or remark the user made during the conversation.

Confirmation before saving applies here as well.

## Where things live

Folders and the abstraction level are set in `knowhow.config.json` at the repository root. Read it before starting. If `knowhow.config.local.json` exists, its values take precedence.

| Key | Meaning | Default |
|---|---|---|
| `knowhow_dir` | Where know-how is saved (the "know-how folder") | `knowhow` |
| `inbox_dir` | Where unprocessed source documents are placed (the "inbox folder") | `inbox` |
| `sensitive_terms_file` | List of proper nouns to detect (the "terms file") | `.sensitive-terms.txt` |
| `abstraction_level` | How far to abstract: `low` (concrete lessons and steps) / `medium` (generalized within the field) / `high` (principles that hold across fields) | `high` |

Relative paths are resolved from the folder holding the config file; absolute paths and `~` also work. With no config file, the defaults apply. If the user names an abstraction level in the request, that takes precedence over the config for that request only. Show the resolved paths and level with:

```bash
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py --show-config
```

## Steps

### 1. Read the input

Read the files or pasted text to the end. When working in the repository, unprocessed material sits in the inbox folder (untracked by git). When only the user's comment is the basis, there is no document to read; treat the comment, and the relevant part of the conversation if needed, as the input.

Do not copy source content into any git-tracked location, and do not quote it there. `_drafts/` holds drafts you wrote, so do not read it as source material. If drafts from an earlier session are still there, ask the user whether to continue from them or discard them.

### 2. Identify the identifying information

Before extracting, take stock of the identifying information in the material. What counts and how to replace it is covered in [references/anonymization.md](references/anonymization.md).

Watch for direct identifiers such as names, and also for **details that identify in combination** (industry + region + size + timing). At this stage also note the structure particular to the material (form fields, classifications, staged procedures) and its distinctive wording, as things not to carry over.

### 3. Collect candidates

When the user's comment is the basis, the claims the user made are the candidates. If several points are mixed together, split them so that each know-how carries one claim. The search hints and exclusions below are for extracting from a document.

From a document, look for the following rather than a summary of it.

- An approach that worked, and why it worked
- A failure or rework, its cause, and how to avoid it next time
- The criterion at a fork in a decision (what was looked at, which way it went)
- Reusable steps, checks, or questions
- A gap between what was expected and what happened

Do not keep:

- Bare records of fact (who decided what and when)
- Circumstances that only hold for that one engagement
- Anything the material does not support and that you could only write by guessing
- Anything with nothing left once the identifying information is removed

A document may yield nothing. Do not force it; report "nothing extracted" with the reason.

### 4. Lift to a concept and write the draft

The candidates are still "events and lessons inside that document". Do not stop at removing proper nouns. Lift them to the configured abstraction level (`abstraction_level`) before writing. The differences between levels, the reasoning, the procedure, and examples are in [references/conceptualization.md](references/conceptualization.md). Read it before writing any draft.

- `high` (default): lift to a **principle** that holds across fields.
- `medium`: field vocabulary is allowed, but write a method and reason that would hold in another organization in the same field. Do not follow the source's structure.
- `low`: keep concrete lessons and steps in a form that can be used directly. Remove proper nouns.

The points below are for `high`. For `medium` and `low`, relax only what the table in the reference allows.

- Put the principle, "why it happens", at the center. Do not write the event; add the lesson from that setting as one of the practices.
- Check that you can explain it without the source's field vocabulary, and that you can name two quite different settings where it applies. If you cannot, it is not lifted far enough.
- If you cannot say when it would not hold, it has gone up into a platitude.
- Merge candidates that come down to the same principle. One document usually leaves one to three. Do not write a draft per candidate.
- Do not carry over the source's item names, ordering, coined terms, numbers, wording, or narrative. Close the document and write from the principle in your own structure.
- For evidence, record only the kind (`basis`) and the count. If the material offers only opinions or impressions, use `opinion`.

When the user's comment is the basis, do not rewrite the claim at a different level. Keep the claim as it is, add any principle you can read from it as a suggestion, and ask at confirmation whether to adopt it.

One know-how = one principle = one file. Follow the format in [references/knowhow-template.md](references/knowhow-template.md).

Do not write into the know-how folder yet. Until the user has confirmed, the text is a draft, and drafts go in `<inbox folder>/_drafts/`. That location is untracked by git and rejected by the pre-commit hook. Never treat the contents of `_drafts/` as source material.

### 5. Check for leaks

Reread the draft as **someone trying to trace it back to its source**. Assume a person who knows the original material, or a third party searching on distinctive wording. Confirming that no proper nouns remain is not enough. Check each point below and rewrite where it applies. For `medium` and `low`, leave out of scope what that level permits (field vocabulary, rounded numbers, item lists at `low`), but still check that the draft is not more concrete than the configured level.

- Do the item names or ordering of a list match the source?
- Does a coined term or unusual phrase from the source remain?
- Do numbers or procedural details remain that have nothing to do with the principle?
- Is there a sentence that paraphrases the source while keeping its word order?
- Is there a paragraph narrating what happened ("in the original case…", "this actually happened when…")?
- Is an example simply the original case?
- Does any practice not follow from the principle (something that is there only because the source said it)? Is the order the same as the flow of the source?
- Do the tags, category, `source_type`, or file name put back the context that the body removed?
- If drafts from the same document are read side by side, can the original event be reconstructed?

Also check that it stands as a concept.

- Can someone in a different setting from the source read it and apply it to their own situation?
- Has it become a platitude that could have been written without the material?

Then run the mechanical check on the drafts.

```bash
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py "<inbox folder>/_drafts"
```

Errors must be resolved. Look at each warning and leave it if it is fine (an official URL for a public tool, for example). The script only catches formal patterns and the words in the terms file, so passing it does not replace the reread above.

For proper nouns in the material that are likely to come up again (the user's own company, key clients, product names), check with the user and add them to the terms file, which is untracked by git. Mention that registering a word that appears often in unrelated contexts, such as a common surname, will cause false positives.

### 6. Compare with existing know-how

Read `INDEX.md` in the know-how folder and the files in the same category to see whether know-how with the same point already exists, and decide how each draft will be handled.

- **New**: add as `<know-how folder>/<category>/<short title>.md`. Prefer an existing category; create one only when none fits.
- **Same point exists**: update the existing file rather than creating one. Add any new condition or counterexample, and update `updated` and `evidence_count`. Rewrite the draft as the full file after the update. If the existing know-how was written at a different abstraction level, ask at confirmation whether to add to it at the existing level or rewrite it at the new one.
- **Contradicts**: do not delete either. Write both as a difference in conditions. If the condition is unknown, say so.

Keep identifying information out of file and category names too.

### 7. Have the user confirm the content

Before saving, show the drafts to the user and ask for confirmation. **Write nothing to the know-how folder or `INDEX.md` until the user says it is fine.**

Only the user, who knows the original engagement and the people involved, can finally judge whether something is identifiable. Do not skip this step even when the mechanical check and your own reread both passed.

Show:

- The **full text** of each draft. No summaries or excerpts. If there are several, number them and separate them clearly.
- For each, one line on what kind of content in the source it came from and what principle it was lifted to (not the event itself), so that the user can say if it was lifted too far or not far enough.
- The abstraction level used (`low` / `medium` / `high`). If non-public material was handled at `low` or `medium`, add that the structure and wording make the source easier to recognize.
- Where each will be saved (category and file name), and whether it is new or an update. For an update, show what changes from the existing content.
- The **kinds** of identifying information removed ("client name, contact name, contract value"), never the values.
- Points you were unsure about (attributes or numbers left in that might identify). If the source is public and several know-how items are being kept, say that the combination of topics may still let someone find the source by searching.
- The parts of the principle and of "when it does not apply" that **the material does not state and you reasoned out yourself**. Lifting to a concept means adding explanation that is not in the source. Separate what rests on the material from your own inference and leave the choice to the user.
- When the user's comment is the basis, **the difference between what the user said and what you added or suggested**. If any items are left unconfirmed (reason, conditions), ask here. Items the user cannot answer may be saved marked as unconfirmed.
- Candidates you did not turn into know-how, and why.

Then ask: "May I save this as it is? If anything is wrong, tell me which draft, where, and how to change it."

Proceed according to the answer.

- **Fine**: go to step 8.
- **Corrections**: revise as directed. Check whether the same problem appears elsewhere in that draft or in the others and fix those too. Redo the checks in step 5, then show the revised full text and what changed, and ask again. Repeat until the user says it is fine.
- **Partly approved**: save only what was approved. Keep revising the rest, or discard it if the user says so.
- **Do not save**: do not save, and delete the drafts.

When a correction is vague ("blur it a bit more"), find out which passage is meant before changing anything. When a reply might or might not be approval, check before saving.

If a correction is a standard that would apply to future extractions as well ("always drop this kind of number"), ask the user whether to reflect it in [references/anonymization.md](references/anonymization.md).

### 8. Save

Save the approved drafts into the know-how folder exactly as approved. Do not edit the content while saving.

- For a new item, add one line to `INDEX.md`. Create `INDEX.md` if it does not exist.
- For an update, fix the line in `INDEX.md` if the gist changed.
- Once saved, delete the corresponding draft from `_drafts/`.

Finally, run the mechanical check on the whole know-how folder.

```bash
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py
```

### 9. Report

Briefly report:

- The know-how added or updated (title and location)
- Anything not saved, or still being revised
- The result of the mechanical check

Commit or push only when the user asks.

## Outside the repository (chat and similar)

Where there is no config file and nowhere to save, do steps 1 to 5 whether extracting from a document or working from the user's comment (drafts are not written to files and the mechanical check cannot run, so do the reread in step 5 with extra care). Then show the full text as in step 7 and ask for confirmation. Revise and show again if corrections come back. Once the user says it is fine, output the final text with a recommended category and file name so the user can save it into the repository.
