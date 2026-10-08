---
name: search-knowhow
description: Search the accumulated know-how and present the items that apply to the situation or question at hand, with sources. Use when the user asks things like "do we have any know-how on…", "look up past lessons", "have we seen something like this before?", "advise me based on our know-how" (in Japanese, 「〜のノウハウある?」「過去の知見を調べて」「前に似たことなかった?」), or wants to check past lessons before starting a proposal, plan, or retrospective.
---

# Search and reference know-how

Find the know-how that applies to the user's situation among what has been accumulated, and present it.

What matters is **not mixing what is in the store with your own general knowledge**. The user wants to know what this repository holds. Filling the gaps with plausible generalities hides whether the store is doing its job and what is missing from it.

## Language

Answer in the user's language. Know-how files may be in any language; frontmatter keys and the fixed values of `basis`, `source_type`, and `abstraction` are in English.

## Where things live

The know-how folder is set by `knowhow_dir` in `knowhow.config.json` at the repository root. Read it before starting. If `knowhow.config.local.json` exists, its value takes precedence. Relative paths are resolved from the folder holding the config file; absolute paths and `~` also work. With no config file, use `knowhow`.

## Steps

### 1. Decide what to look for

Put into words the angles to search from the user's question or situation. If it is a description of a situation ("next week I'm sending a quote to a new client"), break it into the decisions and failures likely to arise there (how to present the quote, first proposals, price negotiation).

If the question is too broad to narrow ("any good know-how?"), show the category structure from `INDEX.md` in the know-how folder and ask which area.

### 2. Find candidates

Read `INDEX.md` in the know-how folder first. It lists every title with a one-line gist, and most candidates turn up there.

Then search the body text to catch what the index misses. Know-how is written as principles that avoid field vocabulary, so the user's wording and field terms often will not match. Translate what is happening in the user's situation (who cannot decide what, what is going missing) into the language of principles before searching. Try several synonyms, broader concepts, and words for related settings.

```bash
grep -rli -e "quote" -e "price" -e "option" "<know-how folder>" --include="*.md"
grep -rl "tags:.*agreement" "<know-how folder>" --include="*.md"
```

Know-how with different wording but the same mechanism (for example, "laying out options changes the kind of decision" applies well beyond quotes) is a candidate even when it sits in another category.

### 3. Read and judge whether it applies

Do not judge from the one line in the index; read the file. Check these in particular.

- **When to use**: Are the conditions for the principle to operate present in the user's situation? Know-how is written as principles usable across fields, so do not exclude something only because the field differs.
- **When it does not apply**: Does the user's situation fall squarely into an exception?
- **evidence_count**: 1 means only "it was so once". Do not treat it with the same weight as something supported several times.
- **abstraction**: `high` is written as a principle across fields, `medium` as a method within a field, `low` as concrete steps for a particular kind of work. When applying `low` or `medium` know-how to another field, note that it may not carry over as it is.
- **basis**: `result` (done and the result confirmed), `opinion` (views or impressions; result not confirmed), or `rule-of-thumb` (the person's experience; reason and conditions not worked out). Say so when presenting `opinion` or `rule-of-thumb` items.
- **updated**: For older items, consider whether the premises (tools, organization, going rates) have changed.

Leave out what does not fit rather than forcing it. For what fits in part, state which part fits and which does not.

### 4. Answer

Reply in this form.

- **Applicable know-how**: In order of relevance, each with its key point, how it applies to the user's situation, and cautions, with a link to the file as the source. Even when there are many, narrow to the few that apply most strongly.
- **Confidence**: Note where the evidence is a single case, or the premises fit only in part.
- **Angles with nothing stored**: State the angles you searched and found nothing for.

When know-how items contradict each other, do not pick one and hide the other; show both and explain the difference in conditions.

If you want to add something from general knowledge, mark it off: "from here on this is general thinking, not accumulated know-how", and keep it separate.

If nothing applies at all, say "nothing found" plainly. Include the words and angles you searched so the user can point you in another direction.

### 5. Feed back into the store

- An angle with nothing stored may be worth capturing in future. Mention in one line that related material can be processed with `extract-knowhow`.
- If the user says "I tried this know-how and it worked / did not work", that is new evidence or a counterexample. Suggest updating the file (`evidence_count`, an addition under "when it does not apply"). When updating, follow `extract-knowhow`'s handling of identifying information.

## Cautions

- Searching and referencing do not change the know-how folder. Suggest updates and make them only after the user agrees.
- Do not write proper nouns from the user's question (client names, contact names) into any file in the repository.
- If you notice a broken link, a file missing from the index, or an index line with no file, report it at the end of the answer.

## Outside the repository (chat and similar)

Where the know-how folder cannot be read, work only from the know-how files the user attached or pasted, and do steps 3 to 5. If nothing was provided, say there is no store to refer to and ask for the know-how files or `INDEX.md`.
