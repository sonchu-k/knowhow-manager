# knowhow-manager

A set of skills for generative AI that takes knowledge you cannot share as it is, extracts the part that can be used as know-how once the identifying information is removed, and lets you save, search, and use it.

## Purpose

Much of what you learn at work is tied to identifying information: client names, the people involved, amounts, how an engagement unfolded. Minutes, proposals, and retrospective notes cannot leave the company as they are, and sometimes cannot even go to another team.

Not everything in them is secret, though. "Why did it go well", "where did the judgment go wrong", "what should we do next time" can be used elsewhere once they are separated from whose story and which engagement it was. What cannot be shared is the identifying information, not the know-how itself.

This repository has generative AI help with that separation, and accumulates the know-how so that it can be reused.

| What it does | Details |
|---|---|
| Extract | Removes identifying information from material or from your own comments, lifts it to a form that holds in other settings, and turns it into know-how. The full draft is shown for confirmation before anything is saved |
| Save | One file per know-how item, with categories and an index. The source material is not saved |
| Search | Describe a situation or ask a question, and the applicable know-how is presented with its source |
| Use | Presents what was found together with how it applies to the current situation and where it does not |
| Policy check | Judges whether the current settings and practice comply with a confidentiality agreement or internal regulation |

Source material stays on your machine (untracked by git); only know-how with the identifying information removed remains in the repository. How far to abstract can be set at one of three levels.

## Skills

| Skill | Role | Example request |
|---|---|---|
| `extract-knowhow` | Creates know-how from material or your own comments and saves it | "Extract know-how from the minutes in inbox" / "Save this as know-how: …" |
| `search-knowhow` | Searches and references accumulated know-how | "Do we have any know-how on quoting?" |
| `check-policy` | Judges whether the settings and practice comply with a confidentiality agreement or internal regulation | "Check whether my current setup is OK under this agreement" |

The skills work in your language: they reply, and write know-how, in the language you use.

## Contents

- [Purpose](#purpose)
- [Skills](#skills)
- [Getting started (first time only)](#getting-started-first-time-only)
- [Extracting know-how](#extracting-know-how)
- [Keeping know-how based on your own comments](#keeping-know-how-based-on-your-own-comments)
- [Abstraction level](#abstraction-level)
- [Searching and referencing know-how](#searching-and-referencing-know-how)
- [Checking against a policy](#checking-against-a-policy)
- [Config file](#config-file)
- [Checks for identifying information](#checks-for-identifying-information)
- [Using it in chat (claude.ai and similar)](#using-it-in-chat-claudeai-and-similar)
- [Layout](#layout)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Getting started (first time only)

You need [Claude Code](https://claude.com/claude-code), git, and Python 3.9 or later (no extra libraries).

```bash
git clone https://github.com/sonchu-k/knowhow-manager.git
cd knowhow-manager

# 1. Enable the pre-commit check
git config core.hooksPath .githooks

# 2. Create the list of proper nouns to detect
cp .sensitive-terms.example.txt .sensitive-terms.txt
```

In `.sensitive-terms.txt`, list the proper nouns that must not remain in know-how, one per line. Putting in your company's name and its short forms, key client names, and internal project and product names lets the mechanical check stop them reliably. The file is untracked by git, so its contents are never shared.

To change where know-how is saved or how far it is abstracted, set up the [config file](#config-file) first.

## Extracting know-how

### 1. Place the material

Put the material in the inbox folder (`inbox/` by default). The folder is untracked by git, and the pre-commit hook also refuses to commit it.

You can also paste the material straight into Claude Code or give it a file path.

### 2. Ask

Open Claude Code in this repository and ask.

```
Extract know-how from the minutes in inbox/
```

```
Capture the lessons from this retrospective (then paste the text)
```

The skill works in this order.

1. Reads the material and identifies the identifying information (names, companies, amounts, dates, places)
2. Collects candidates: approaches that worked, failures and their causes, decision criteria
3. Lifts the candidates to the configured [abstraction level](#abstraction-level). At the default (`high`) it lifts them to principles, merges the ones that come down to the same principle, and writes in its own words and structure
4. Rereads as someone trying to trace the text back to its source, and runs the mechanical check
5. Compares with existing know-how and decides whether each item is new or an update to an existing file
6. Shows the full drafts and asks whether to save

Nothing has been saved at this point. Drafts are kept in `<inbox folder>/_drafts/` (untracked by git).

Some material yields "nothing extracted". Material that is only a record of facts, or that has nothing left once the identifying information is removed, is not forced into know-how.

### 3. Check the content and answer

Read the drafts and check:

- that nothing remains from which the original company, person, or engagement could be guessed
- that someone who does not know the source could read it and act differently

Along with the drafts you are shown:

- the abstraction level used, and what kind of content was lifted to what principle
- where each will be saved, and whether it is new or an update (and what changes, for an update)
- the kinds of information removed
- the parts the material does not state and the skill reasoned out (the explanation of the principle, "when it does not apply", and so on)
- points the skill was unsure about, and candidates it did not turn into know-how

The mechanical check only catches formal patterns and registered terms, and only someone who knows the original engagement can finally judge whether something is identifiable, so do not skip this.

- **If it is fine**, answer "fine" or "save it". The know-how is saved in the know-how folder (`knowhow/` by default) and the index is updated.
- **If something is wrong**, say where and how to change it. You are shown the revised full text and what changed, and asked again. Nothing is saved until you say it is fine.

  ```
  In no. 2, "a department of a dozen or so people" is identifiable, drop it. Don't save no. 3. No. 1 is fine as it is.
  ```

You can also approve only some, or decide not to save.

### 4. Commit

```bash
git add knowhow/
git commit -m "Add know-how"
```

### What a know-how file looks like

One know-how = one principle = one file, saved as `<know-how folder>/<category>/<title>.md`. The index is `INDEX.md`.

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
## Principle
## When to use
## How
## When it does not apply
## Evidence
```

- `basis` is the kind of evidence: `result` (done and the result confirmed), `opinion` (based on views or impressions; result not confirmed), `rule-of-thumb` (the person's experience; reason and conditions not worked out).
- `evidence_count` is the number of mutually independent documents or occasions that support the know-how. One document counts as one however many cases it contains. Read 1 as "it was so once".
- `abstraction` is the abstraction level the know-how was written at.
- `source_type` holds only a broad class: `document`, `meeting-or-conversation`, `own-comment`.
- The title, body, and section headings are written in your language. Frontmatter keys and the fixed values above stay in English.

## Keeping know-how based on your own comments

Instead of having generative AI work out the content, you can keep know-how based on your own thinking and experience.

**From a comment alone, with no document**

```
Save this as know-how: always present three quotes. With only one it becomes accept-or-refuse, and if the price is a sticking point the deal just dies
```

**Adding your own reading or angle to a document**

```
About the retrospective in inbox/: I think the main lesson is that we never visited the site before fixing the requirements. Turn that into know-how
```

```
From these minutes, extract only the points about price negotiation
```

**From the exchange during work**

```
Turn that last point into know-how
```

In these cases the skill takes the role of organizing the stated claim and putting it into the format.

- It does not swap the claim for something else or for a generality. Any principle it can read from the claim is added as a suggestion, and you are asked whether to adopt it.
- It does not fill in unstated reasons or conditions by guessing. Unknown items are written as "not confirmed" and asked about at confirmation. If you do not know, they can be saved as they are.
- If you name an angle, it stays within it. If the document holds other useful points, you are asked whether to keep them.
- If your reading and the document disagree, you are told.

Removing identifying information and confirming before saving work the same as when extracting from a document. At confirmation, what you said and what the skill added are shown separately.

## Abstraction level

Text with only the proper nouns removed is "a record of an event whose owner is unknown": hard to use in another field, and its structure and wording still show where it came from. When taking know-how out of an event, this skill lets you choose how far to abstract.

### Four stages of abstraction

| Stage | Content | Example |
|---|---|---|
| Event | Who did what and what happened | The first quote met resistance, but when three plans were presented side by side they agreed on the middle one |
| Lesson from that setting | What to do in the same setting | Present three quotes |
| Principle | Why it happens | With one option the decision is "accept or refuse"; with several it becomes "which one" |
| Platitude | Something true of anything | Make proposals from the other party's point of view |

Events are not kept as they are, and nothing is turned into a platitude. The setting decides where in between the center sits.

### The three levels

Choose with `abstraction_level` in `knowhow.config.json`. The default is `high` (maximum).

| | `low` concrete | `medium` generalized within the field | `high` principle (maximum) |
|---|---|---|---|
| What remains | Concrete lessons and steps. Forms and item lists remain too | Methods and reasons that work in that field | Principles that hold across fields |
| Example | Present three quotes, good / better / best, with the one you want chosen in the middle | Present several quotes side by side. With one, resistance to the price becomes refusal | With one option the decision is "accept or refuse"; with several it becomes "which one" |
| Field vocabulary | Used | Used | Not used |
| Numbers | May stay, rounded | Only those needed to explain the reason | Left out unless the principle depends on them |
| Items kept per document | Several or more | Two to four | One to three |
| Chance of being traced back | High | Medium | Low |
| Suited to | A procedure collection for a team that repeats the same work; public source material | Sharing within the same profession or field | Sharing across fields; when the origin must not show |

At every level, proper nouns are removed, the mechanical check runs, and you confirm before saving. The level used is recorded in each know-how item's `abstraction` field.

### How `high` is written

- The principle sits at the center; the lesson from that setting is added as one of the practices.
- The source's item names, ordering, coined terms, numbers, wording, and narrative are not carried over.
- Only practices that follow from the principle are listed.
- Candidates that come down to the same principle are merged into one item.
- The explanation of the principle and "when it does not apply" are often not in the material and are reasoned out by the skill. At confirmation they are shown separately from what rests on the material.

### Changing the level

- **Change the setting**: edit `abstraction_level` in `knowhow.config.json` (or `knowhow.config.local.json` for your own machine only).
- **Change it once**: name it in the request. It takes precedence over the setting.

  ```
  Extract know-how from the procedure notes in inbox/. Use abstraction level low
  ```

- **Adjust at confirmation**: if a draft seems lifted too far (a platitude) or not far enough (still the event), say so and have it revised.

### Choosing a level

At `low` and `medium`, structure and wording stay closer to the source, so someone who knows the source can recognize the origin more easily. `high` is recommended for non-public material. For the ways in which even `high` is not complete, see [Limits](#limits).

## Searching and referencing know-how

Describe the situation or ask the question as it is.

```
Next week I'm sending a quote to a new client. Any relevant know-how?
```

```
The client is slow to reply and the project is stuck. Have we learned anything similar before?
```

```
Review this migration plan in light of our know-how on data migration
```

The skill searches the index and the body text, including rewordings, and returns what applies with links to the source files.

- What is in the store and any addition from general knowledge are shown separately.
- Items supported by a single case, items whose evidence is only an opinion or rule of thumb, and items whose premises fit only in part are marked as such.
- Know-how is written as principles, so an item can be a candidate even when its field differs from the question, as long as the same principle operates.
- If nothing applies, "nothing found" is returned with the angles that were searched.

Searching alone does not change any know-how. If you say "I tried this know-how and it worked / did not work", an update to the file is suggested.

## Checking against a policy

Hand over a confidentiality agreement, internal regulation, generative-AI usage rule, or similar, and the skill judges clause by clause whether the current settings and practice comply, with reasons and options.

### How to use it

Put the policy document in the policy folder (`policies/` by default, untracked by git) or paste it, and ask.

```
Check whether my current setup is OK under the non-disclosure agreement in policies/
```

```
Under this internal regulation, may I turn minutes into know-how? (then paste the text)
```

### What is compared

Know-how management is divided into four stages, and each clause is matched to the stages it touches.

| Stage | What happens | Related settings and facts |
|---|---|---|
| A. Storage | Source material is kept locally | Location of the inbox folder, cloud sync, files left after processing |
| B. Input | Source material is read by a generative-AI service | The service used and its contract terms (not knowable from the settings, so you are asked) |
| C. Accumulation | Abstracted know-how is saved | `abstraction_level`, location of the know-how folder, remote repository, registered terms, the hook |
| D. Use | Know-how is used in another setting or in work for another organization | `abstraction_level`, the level of the know-how already saved |

The settings and storage state can be gathered with this command (the skill runs it itself).

```bash
python3 .claude/skills/check-policy/scripts/policy_facts.py
```

### Reading the result

Each clause gets one of the following, with the clause number and the reason.

| Judgment | Meaning |
|---|---|
| Compliant | What the clause requires is met by the current settings and practice |
| Not compliant | The current settings and practice do not meet it |
| Cannot determine | The wording does not settle it, part of the policy is missing, or a needed fact is unknown |

The overall judgment is "compliant", "conditional", or "not compliant", and the options are presented in three groups.

1. What a settings change can address (raising `abstraction_level`, moving storage, and so on)
2. What a change in practice can address (not entering certain material, deleting source material after processing, and so on)
3. What needs to be confirmed (who to ask and what)

The config file is not edited until you agree.

### Things to know

- **It is not a legal judgment.** It is groundwork to reduce oversights. A clause in doubt becomes "cannot determine", not "compliant". The final decision rests with you and each organization's legal or secretariat function.
- **Some stages cannot be addressed by abstraction.** Source material is sent to the generative-AI service in its form before abstraction (stage B). No value of `abstraction_level` addresses a policy that prohibits entering material into external services.
- **Removing proper nouns does not necessarily stop something being confidential information.** Under a policy that includes derivatives and analyses in confidential information, know-how lifted to a principle may still be covered.
- **Reading the policy is itself an input.** The policy document may be confidential under its own terms; the report says that it was read with generative AI and that this was not judged.
- **With several policies**, each is judged separately. The settings are shared, so they have to meet the strictest one.
- The policy documents cannot be shared either, so the policy folder is untracked by git and rejected by the pre-commit hook.

## Config file

Where know-how is saved, where source material and policies are placed, and the abstraction level are set in `knowhow.config.json`.

```json
{
  "knowhow_dir": "knowhow",
  "inbox_dir": "inbox",
  "sensitive_terms_file": ".sensitive-terms.txt",
  "policies_dir": "policies",
  "abstraction_level": "high"
}
```

| Key | Meaning | Default |
|---|---|---|
| `knowhow_dir` | Where know-how is saved. The index `INDEX.md` lives here too | `knowhow` |
| `inbox_dir` | Where unprocessed source material is placed | `inbox` |
| `sensitive_terms_file` | List of proper nouns to detect | `.sensitive-terms.txt` |
| `policies_dir` | Where confidentiality agreements and internal regulations are placed | `policies` |
| `abstraction_level` | Abstraction level (`low` / `medium` / `high`). See [Abstraction level](#abstraction-level) | `high` |

- Relative paths are resolved from the folder holding the config file. Absolute paths and `~` also work, so locations outside the repository (an Obsidian vault, for example) can be used.
- Keys you leave out take their defaults.
- An unknown key, or an `abstraction_level` other than the three values, is a config error.

### Changing settings for your machine only

Create `knowhow.config.local.json` in the same format; only the keys you write are overridden. The file is untracked by git.

```json
{
  "knowhow_dir": "~/Documents/vault/knowhow",
  "inbox_dir": "~/Documents/vault/_sources"
}
```

### Checking after a change

```bash
python3 .claude/skills/extract-knowhow/scripts/check_sensitive.py --show-config
```

The resolved paths and the abstraction level are shown. Folders that do not exist are marked "(does not exist)", and a warning appears if the inbox folder or the policy folder is tracked by git.

### Cautions when changing

- If you move `inbox_dir` or `policies_dir` to another folder inside the repository, add that folder to `.gitignore` as well.
- If `knowhow_dir` is outside the repository, this repository's pre-commit hook does not cover it. Run the mechanical check by hand.
- Existing know-how is not moved automatically. When changing the folder, move it yourself together with `INDEX.md`.

## Checks for identifying information

Five safeguards are layered to keep identifying information out.

1. **Removing proper nouns**: identifying information is identified before extraction and replaced with roles and descriptions.
2. **Lifting to a concept**: the shape of the event (structure, wording, narrative) is not kept; the text is rewritten from the principle and then reread as someone trying to trace it back. How far depends on the [setting](#abstraction-level).
3. **Mechanical check**: detects formal patterns and registered terms.
4. **Confirmation before saving**: you read the full draft, and nothing is saved until you say it is fine.
5. **Pre-commit hook**: runs the mechanical check on changes to the know-how folder and refuses to commit files in the inbox folder or the policy folder.

### What the mechanical check detects

| Class | Target | Handling |
|---|---|---|
| Error | Email addresses, phone numbers, postal codes, IP addresses, registered terms | The commit is blocked until resolved |
| Warning | Corporate suffixes (株式会社, Inc., and so on), URLs, names with honorifics | Look and decide. The commit is not blocked |

The phone number, postal code, and honorific patterns target Japanese text. For other languages, rely on registered terms.

### Running it by hand

```bash
S=.claude/skills/extract-knowhow/scripts/check_sensitive.py

python3 $S                    # the whole know-how folder
python3 $S path/to/file.md    # a particular file or folder
python3 $S --strict           # treat warnings as errors
python3 $S --show-config      # show the settings
```

Exit codes: 0 = clean, 1 = possible identifying information, 2 = bad settings or arguments.

### Limits

- **The mechanical check** cannot detect what is identifiable from context (a combination of industry, region, size, and timing) or proper nouns that are not registered. Passing it does not mean safe, so use it together with confirmation before saving. Add new proper nouns to `.sensitive-terms.txt` as they come up. Registering a word like a common surname raises errors in unrelated contexts too.
- **Removing proper nouns is not enough.** In a trial with public material, with every proper noun removed, the original documents were still found by searching when item names, ordering, unusual phrases, and incidental numbers remained. `high` is written so as not to carry these over.
- **Even `high` is not complete.** When several know-how items are kept from the same document, the combination of topics can narrow down the source. A public source may still be found by searching, and with non-public material the people who have read it may be able to guess. Keeping fewer items makes it harder.

## Using it in chat (claude.ai and similar)

Zip each skill folder and upload it as a skill.

```bash
cd .claude/skills
zip -r extract-knowhow.zip extract-knowhow
zip -r search-knowhow.zip search-knowhow
zip -r check-policy.zip check-policy
```

- **Extract**: attach a file and ask "extract know-how from this". The know-how is shown in the same format and you are asked to confirm. Once you say it is fine, the final text is output with a recommended category and file name; save it into the know-how folder. The mechanical check does not run in chat, so run it in the repository after saving.
- **Abstraction level**: chat has no config file, so the default `high` applies. Name the level in the request to change it.
- **Policy check**: the settings cannot be gathered automatically, so you are asked for the abstraction level, storage locations, and the generative-AI service used.
- **Search**: the know-how folder cannot be read from chat, so attach the know-how files or `INDEX.md` when asking.

## Layout

```
knowhow.config.json          Folder locations and the abstraction level
knowhow/                     Accumulated know-how (<category>/<title>.md)
  INDEX.md                   Index
inbox/                       Unprocessed source material (untracked by git)
policies/                    Confidentiality agreements and internal regulations (untracked by git)
.claude/skills/extract-knowhow/
  SKILL.md                   Extraction procedure
  references/                Handling identifying information, abstraction levels and lifting, file format
  scripts/check_sensitive.py Mechanical check for identifying information
.claude/skills/search-knowhow/
  SKILL.md                   Search and reference procedure
.claude/skills/check-policy/
  SKILL.md                   Procedure for judging against a policy
  references/                What to look at in a policy, guide to judging by level
  scripts/policy_facts.py    Gathers the settings and storage state
.githooks/pre-commit         Runs the mechanical check at commit time
.sensitive-terms.example.txt Template for the registered terms list
CLAUDE.md                    Working rules for Claude Code
```

`knowhow/`, `inbox/`, and `policies/` are the default locations and can be changed in the config.

## Troubleshooting

**The commit stops with "Possible source material or identifying information found"**
Fix the lines shown as `ERROR`. For a false positive from a registered term (a common word was registered, for example), remove the word from `.sensitive-terms.txt`.

**The commit stops with "files under inbox_dir (or policies_dir) cannot be committed"**
Source material or a policy document is staged. Unstage it with `git restore --staged <file>`.

**The hook does not run**
Check that `git config core.hooksPath` prints `.githooks`. It has to be set again after a fresh clone.

**"config error: nothing to check at: …"**
The `knowhow_dir` folder does not exist. Check the path with `--show-config`, then create the folder or fix the setting.

**"config error: … abstraction_level must be one of low / medium / high"**
The value of `abstraction_level` in the config file is none of the three. Fix it.

**The extracted know-how is too abstract or too concrete**
For a one-off, say "more concrete" or "this part is identifiable" at confirmation and have it revised. If it is always the case, change `abstraction_level`. To adjust the standards themselves, edit `conceptualization.md` (abstraction) and `anonymization.md` (identifying information) under `.claude/skills/extract-knowhow/references/`.

**Drafts are left in `_drafts/`**
Work was interrupted during confirmation. The next time you ask for an extraction, you are asked whether to continue from them or discard them. Delete them if they are not needed.

**Search finds nothing**
Ask again in other words, or look at `INDEX.md` directly. If the area really has nothing stored, extract from related material to build it up.

## License

[MIT License](LICENSE)
