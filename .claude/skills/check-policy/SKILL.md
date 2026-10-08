---
name: check-policy
description: Read rules such as a confidentiality agreement, non-disclosure clause, internal regulation, information-handling policy, or generative-AI usage guideline, and judge clause by clause whether the current know-how management settings (abstraction level, storage locations, and so on) and working practice are enough to comply, giving reasons and options for each. Use when the user says things like "is my current setup OK under this agreement?", "check the settings against this policy", "can I turn this material into know-how?" (in Japanese, 「この契約で今の設定は大丈夫?」「規程に照らしてチェックして」「規定チェックして」), or has received a new set of rules and wants to review the settings.
---

# Policy check

Read a confidentiality agreement or internal regulation and judge whether the current know-how management settings and practice comply with it.

This is **groundwork to reduce oversights**, not a legal judgment. How a contract is read depends on the counterparty and the governing law. The most important commitment of this skill is never to say "compliant" where there is doubt, and to leave the final decision to the user and each organization's legal or secretariat function. Wrongly saying "compliant" does far more harm than saying "cannot determine".

## Language

Report in the user's language. Quote clauses in the language they are written in.

## Where things live

Policy documents go in the folder set by `policies_dir` (default `policies`) in `knowhow.config.json` at the repository root. If `knowhow.config.local.json` exists, its value takes precedence. The folder is untracked by git and rejected by the pre-commit hook.

The policy documents are themselves confidential.

- Do not copy policy text into any git-tracked file.
- In answers, quote only the short span needed to support a judgment, and refer to clauses by number.
- Do not write the counterparty's name in commit messages or know-how.

## Steps

### 1. Read the policy

Read the file the user named, the pasted text, or the documents in the policy folder, to the end. If there are several, confirm with the user which ones are in scope.

The policy document may itself be confidential information under its own terms. Reading it means it has been entered into a generative-AI service, so state in the "assumptions and limits" of the report that the policy text was read with generative AI and that whether this conflicts with the policy has not been judged.

If it looks as though only part of the policy was provided (no definitions clause, references to an appendix), note that and give it as a reason for "cannot determine" when judging.

### 2. Gather the current settings and practice

Gather the settings and storage state with:

```bash
python3 .claude/skills/check-policy/scripts/policy_facts.py
```

Also check what each abstraction level leaves behind, using the table in `.claude/skills/extract-knowhow/references/conceptualization.md`. Do not judge from the name of the setting; judge from what actually remains in know-how at that level.

The last part of the command's output, "not knowable from here", lists facts to ask the user about, only where they affect a judgment. For anything left unanswered, do not guess; mark it "cannot determine".

### 3. Pick out the relevant clauses

Think of know-how management as four stages, and see which stage each clause touches.

| Stage | What happens |
|---|---|
| A. Storage | The source document is kept locally in the inbox folder |
| B. Input | The source document is read by a generative-AI service |
| C. Accumulation | Know-how, with identifying information removed and abstracted, is saved (including to a remote repository) |
| D. Use | Accumulated know-how is used in another setting or in work for another organization |

The kinds of clause to look for and what to check in each are in [references/checkpoints.md](references/checkpoints.md). Read it before picking out clauses.

### 4. Judge each clause

Give each relevant clause one of three judgments.

| Judgment | Meaning |
|---|---|
| Compliant | Comparing what the clause requires with the facts of the settings and practice, it can be said to be met |
| Not compliant | The current settings and practice do not meet what the clause requires |
| Cannot determine | The wording does not settle it, part of the policy is missing, or a fact needed for the judgment is unknown |

Rules for judging:

- Cite the clause by number and quote briefly as needed.
- State which setting value and which fact the judgment rests on.
- When it is unclear whether the wording reaches abstracted know-how, use "cannot determine". Do not reach "compliant" by reasoning that "it was abstracted to a principle, so it cannot be confidential information".
- Do not read silence as permission.
- When one clause touches several stages, judge each stage separately (storage compliant, input not compliant, and so on).
- "Cannot determine" is for unclear wording and unknown facts. Where the wording is clear, the facts are known, and the requirement is not met, say "not compliant". For example, if a clause limits use of confidential information to the performance of a particular role, and material that is plainly confidential is read in order to build know-how for reuse elsewhere, the input and accumulation stages are "not compliant". Whether using the abstracted know-how elsewhere (stage D) falls under the same clause depends on whether the know-how counts as confidential information; if the wording does not settle that, use "cannot determine".

### 5. Give the overall judgment and options

Choose the overall judgment from three.

- **Compliant**: every relevant clause is "compliant".
- **Conditional**: no "not compliant", but some "cannot determine"; or compliance can be reached by changing settings or practice.
- **Not compliant**: some clause cannot be met by changing settings (the material must not be processed, the counterparty's permission is needed, and so on).

Present the options in this order.

1. **What a settings change can address**: changing `abstraction_level`, moving storage, adding registered terms, enabling the hook. Say what changes as a result.
2. **What a change in practice can address**: not entering certain kinds of material, deleting source documents after processing, keeping fewer items.
3. **What needs to be confirmed**: who to ask and what, specifically (ask the counterparty's secretariat whether this wording in the clause covers derivatives, for example).

Do not edit the config file until the user agrees.

### 6. Report

Use this structure.

- **Overall judgment** and the main reason for it
- **Judgment per clause**: a table of clause, what it requires, stage, current setting or fact, judgment, reason
- **Options**: the three groups above
- **Assumptions and limits**: the extent of the policy provided, facts that remained unknown after asking, and that this is not a legal judgment

If the user wants, save the report to `<policy folder>/_reports/` (untracked by git).

## Several policies

Judge each policy separately. The settings are shared by all material, so they have to meet the strictest policy. When policies differ greatly in strictness, offer, alongside matching the settings to the strictest, the option of treating only the material that policy covers differently (naming the level per request, or not processing it).

Information obtained under one policy may end up being used in work related to the counterparty of another (stage D). This matters especially for someone who works with several organizations. Read the clauses on use outside the stated purpose and on disclosure to third parties from this angle too.

## Outside the repository (chat and similar)

The command that gathers settings is not available. Ask the user for the abstraction level, where source documents and know-how are kept, and which generative-AI service is used, then carry out step 3 onward. For anything left unanswered, use "cannot determine".
