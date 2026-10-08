# What to look at in a policy

The kinds of clause to pick out, which stage of know-how management they touch (A storage / B input / C accumulation / D use), and what to check when judging. Pick up clauses of kinds not listed here too, if they touch any of the four stages.

## Kinds of clause

| Kind of clause | Stage | What to check |
|---|---|---|
| Definition of confidential information | All | What counts. Whether oral information and things learned in meetings are included. Whether marking as confidential is required |
| Derivatives and analyses | C, D | Whether summaries, analyses, notes, or derivatives made from confidential information are included in it. If so, abstracted know-how may be covered |
| Residual information | C, D | Whether general knowledge, experience, and skills retained in memory may be used freely. Even if so, check separately whether writing them down is allowed |
| Exclusions | C, D | Whether public information or independently obtained information is excluded. Having abstracted something is usually not a ground for exclusion |
| Use outside the stated purpose | B, C, D | Whether the purposes for which confidential information may be used are limited. Whether accumulating it as know-how and using it in other work falls within them |
| Disclosure or provision to third parties | B, C | Whether entering material into a generative-AI service or saving it to a cloud repository may count as disclosure or provision. Whether there are terms on contractors and external services, or a prior-consent requirement |
| Limits on copying, storage, and removal | A, C | Whether copying is allowed, any specified storage location or method (company systems only, encryption, no personal devices), limits on taking material off premises |
| Return and destruction | A, C | Duty to return or destroy material and copies at the end of the contract or on request. Whether files left in the inbox folder, drafts, and know-how are covered |
| Rules on generative AI and external services | B | Approved services, classes of information that may be entered, a requirement that inputs not be used for training, approval procedures |
| Personal information | A, B, C | Handling of material containing personal information; limits on provision to third parties and transfer abroad |
| Undisclosed material facts | B, C, D | Handling of undisclosed facts that affect investment decisions and information subject to trading rules. Even when abstracted, it can be a problem if it can be inferred from timing or context |
| Competition and conflicts of interest | D | Limits on using what was learned at one organization in work for a competing one |
| Term | All | How long the obligations last, and whether they survive the end of the contract |
| Reporting and incident response | All | Duty to report a leak or a risk of one |

## Abstraction level and a rough guide to judging

Reason from what remains at the configured level. The following is a guide; the wording of the clause takes precedence.

| What the clause says | `low` | `medium` | `high` |
|---|---|---|---|
| Prohibits disclosing or copying the confidential information itself (no mention of derivatives) | Concrete steps and items remain; tends toward not compliant | Field and method remain; tends toward cannot determine, depending on wording | The shape of the original does not remain. Whether it reaches derivatives depends on wording; may be cannot determine |
| Includes derivatives and analyses in confidential information | Not compliant | Not compliant, or cannot determine | Cannot determine (even lifted to a principle, it may count as something made from the information) |
| Allows free use of residual information | Written-down concrete steps usually go beyond residual information | Cannot determine | Tends toward compliant. Check whether writing it down is allowed |
| Prohibits disclosing information that identifies a particular counterparty or engagement | Origin is easy to recognize; tends toward not compliant | Cannot determine | Tends toward compliant. Weaker when several items come from one document or the source is searchable |

## What no level changes

The following are the same whatever the abstraction level is set to. If a clause restricts them, no settings change can address it.

- **Stage B (input)**: The source document is sent to the generative-AI service in its form before abstraction. If a policy prohibits entering material into external services, or requires approval, that has to be dealt with regardless of the level.
- **Stage A (storage)**: The source document stays in the inbox folder after processing. Rules on storage location and on return or destruction are addressed by practice (moving the folder, deleting after processing), not by settings.
- **Where stage C saves to**: If the know-how folder is connected to a remote repository, the know-how sits on an external service.

## Where judgments go wrong

- Thinking "the proper nouns are gone, so it is not confidential information". Most policies decide confidentiality by the content of the information, not by whether a name is present.
- Reading the absence of a rule as permission.
- Stretching a residual-information clause to cover writing things down and accumulating them.
- Judging stage B compliant without checking the terms of the generative-AI service (whether inputs are used for training, where they are stored).
- Judging the whole policy after reading only part of it.
- Asking generative AI to strip out information of a class that must not be entered. Asking for the stripping is itself the input. The user has to remove those parts before anything is read.
- Overlooking the case where the generative-AI contract is in the name of one of the organizations involved. Another organization's confidential information would then enter a service under that organization's control.
