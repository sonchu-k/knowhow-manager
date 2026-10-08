# Lifting to a concept

Text with only the proper nouns removed is "a record of an event whose owner is unknown". It is hard to use in another setting, and because its structure and wording are unchanged, anyone who knows the source can tell where it came from.

What should remain is the **principle taken from the event**, not the event. Lifting to a principle makes the result usable in other fields and erases the shape of the source at the same time. That is where reusable and not identifiable are both achieved.

## Abstraction level (setting)

How far to lift is set by `abstraction_level` in `knowhow.config.json`. The values are `low`, `medium`, and `high`; the default is `high`. If the user names a level in the request ("use low this time"), follow that for that request only.

| | `low` concrete | `medium` generalized within the field | `high` principle (maximum) |
|---|---|---|---|
| What sits at the center | The lesson from that setting and concrete steps (stage 1 in the table below) | A method that works within the field, and its reason (between stages 1 and 2) | A principle that holds across fields (stage 2) |
| Field vocabulary | Used | Used | Explained without it |
| Transfer check | Would it work on the next engagement of the same kind? | Would it work for another organization or engagement in the same field? | Can you name two settings in quite different fields? |
| Lists, forms, procedures | May stay in a directly usable form | Narrow to what is needed; rewrite in your own words and order | Do not copy. Write the principle of why they are needed |
| Numbers | May stay, rounded to order of magnitude or ratio | Only those needed to explain the reason, rounded | Leave out unless the principle depends on them |
| Narrative of what happened | A short account with identifying information removed is acceptable | Leave out. Explain the cause and effect instead | Leave out. Explain the cause and effect instead |
| Examples | The original case, generalized, is acceptable | A general example from the same field | An illustrative example from a different field |
| Typical number kept per document | One per candidate (several or more) | Merge similar ones; two to four | One per principle; one to three |
| Chance of being traced back | High | Medium | Low (remains for public sources) |
| Suited to | A procedure collection for a team that repeats the same work; public source material | Sharing within the same profession or field | Sharing across fields; when the origin must not show |

What does not change with the level:

- Proper nouns and identifiers are removed by the standard in [anonymization.md](anonymization.md).
- Never write a platitude that applies to anything (stage 3).
- When you add content that is not in the material, mark it separately at confirmation.
- Run the mechanical check and get the user's confirmation before saving.
- Record the level used in the know-how's `abstraction` field.

At `low` and `medium`, structure and wording stay closer to the source, so someone who knows the source or searches for it can recognize the origin more easily. When non-public material is processed at `low`, tell the user so at confirmation.

The sections "Lifting procedure" and "Do not carry over the shape of the source" below are written for `high`. For `medium` and `low`, relax only what the table above allows.

## Stages of abstraction

| Stage | Content | Example (fictional) |
|---|---|---|
| 0 Event | Who did what and what happened | The first quote met resistance, but when three plans were presented side by side they agreed on the middle one |
| 1 Lesson from that setting | What to do in the same setting | Present three quotes |
| 2 Principle | Why it happens; a mechanism that holds when the setting changes | With one option the other party's decision is "accept or refuse"; with several it becomes "which one". When you want a decision, present things in a form that changes the kind of decision |
| 3 Platitude | Something true of anything | Make proposals from the other party's point of view |

The center of the know-how is **stage 2**.

- Do not write stage 0. Keep only the kind and count of evidence.
- Add stage 1 as one of the practices under the principle.
- At stage 3 the content could be written without the material, and reading it changes nothing.

## Lifting procedure

Think through each candidate in this order. Do steps 1 to 4 in your head; do not leave the intermediate reasoning in the draft.

1. **Put the event in one sentence.** What was done, and what came of it.
2. **Say why it turned out that way without using the vocabulary of the source's field.** If you can explain it without words like "incident", "quote", or "tender", you have a candidate principle. If you cannot explain it without them, it is still a paraphrase of the event.
3. **Try transferring it.** Think of two settings quite unlike the source and check whether the same principle operates there. If you cannot name two, it is still at stage 1; go up one more.
4. **Check that it has not gone too far.** Try to say when it would not hold. If you cannot, or if you could have written it without reading the material, it has reached stage 3. Add the condition under which it holds and come down one.
5. **Merge candidates that reach the same principle, and narrow the number.** Many of the candidates from one document are different appearances of the same principle. Make one item per principle and turn the individual candidates into practices. One document usually leaves one to three. Know-how made from the same document shares dates and style, so it is easy to see it shares an origin, and the combination of topics narrows down the source. The more items, the easier that is, so drop the ones that are weak as principles or overlap with others and keep only the strong ones.
6. **Write without carrying over the shape of the source.** See the next section.

## Do not carry over the shape of the source

Write the principle in your own words and your own structure. Each of the following is a clue to the origin even with no proper nouns left.

| Do not carry over | Why, and what to do instead |
|---|---|
| Item names, classification names, ordering | The shape of a list is a fingerprint. Even if the source has a ten-field form, do not copy it. Write the principle of why those fields are needed, and name only the necessary ones in your own words |
| Coined terms, unusual phrases | Combined with an ordinary topic word, they pin the source down in a search. Replace with common words |
| Numbers and procedural details off the main point | A detail like "two sessions, two hours in total" is left out unless the principle depends on it |
| Paraphrases of statements or text | A paraphrase that keeps the word order becomes decisive once the source has been found. Close the material and write from the principle |
| Narrative of what happened | Paragraphs like "in the original case…" or "this actually happened when…" keep the event intact. Do not write them. Explain the cause and effect in general form |
| Examples that use the original case | If an example is needed, make up an illustrative one from a different field. Introduce it with "for example" and do not write it as if it really happened |
| Practices that do not follow from the principle | An item that is there only because the source said it, with a weak link to the principle (the source's future plans, one person's impression), is a strong search clue and also dilutes the focus. List only practices that follow from the principle as "therefore do this" |
| Ordering that follows the flow of the source | If the practices are listed in the order of the source's chapters or timeline, they can be matched even when reworded. Reorder by importance from the principle's point of view and merge similar ones |
| Tags or classification that restore context | Do not put the industry, role, or kind of engagement removed from the body back in through tags, category, or `source_type` |

## When the source is public

A public article or set of minutes can sometimes be found by searching on the combination of topics even after every proper noun and all of its shape is gone. Lifting to the level of principle and narrowing the number makes it harder to find, but cannot prevent it entirely. When the source is public and several know-how items are being kept, tell the user so at confirmation. The same applies to non-public material with respect to people who have read it.

## Example (fictional)

**What the source said**

> The incident report form was changed from five fields, "date and time, course of events, cause, action taken, future measures", to ten: "summary, impact, root cause, trigger, recovery, detection, permanent measures, lessons, timeline, analysis". With the old form, the cause field ended at the name of the symptom, and nobody wrote down what had gone well.

**Bad: proper nouns removed, shape unchanged**

> Give the incident review form ten fields: summary, impact, root cause, trigger, recovery, detection, permanent measures, lessons, timeline, analysis. The old form had five, and causes ended at the symptom name.

Item names and order are the source's, and the field and the narrative both remain. People in other fields cannot use it, and anyone who knows the source recognizes it at once.

**Good: lifted to a principle**

> **Key point**: Information with no field on the form does not get recorded. If there is information you want kept, give it a field of its own instead of leaving it to free text.
>
> **Principle**: People treat filling in the fields as the end of the task. With no field, there is no reason to write that information and nothing to prompt the writer when it is missing. With a field, a blank becomes a signal that the matter has not been thought about yet.
>
> **When to use**: Reports, applications, minutes, handover notes, anywhere information is collected in a set format and a particular kind keeps going missing.
>
> **How**: Name the missing information specifically and give each its own field. Where two things are similar but different (the immediate trigger and the underlying cause), separate the fields so they do not blur.
>
> **When it does not apply**: More fields mean more effort, and filling them in tends to become the goal. Imposing the same form on every case does not last.

It works for incident reports, sales daily reports, and handover notes alike. None of the source's item names or narrative remain.

**Bad: lifted too far**

> Design record formats to suit their purpose.

There is no case where it fails to hold, and it could be written without the material.

## When the user's comment is the basis

The claim is the user's, so do not rewrite it at another level on your own.

- Keep the user's claim (usually in the form of stage 1) as it is, under the key point or the practices.
- If you can read a principle from it, add it **as a suggestion** and ask at confirmation: "Put more broadly, I understand the principle to be this; may I write it that way?" The user decides.
- If the user gave no principle and you cannot state one with confidence, write "principle not confirmed (rule of thumb)".

## How to write the evidence

Do not narrate the event. Record only the **kind and count** of evidence. Put the kind in `basis` as one of:

| `basis` | Meaning |
|---|---|
| `result` | It was actually done and the result was confirmed |
| `opinion` | Based on the views or impressions of those involved or present. The result is not confirmed |
| `rule-of-thumb` | Based on the person's own experience, with reason and conditions not worked out |

If the material offers only opinions or impressions, say `opinion` honestly. Do not use `result` because the principle looks coherent.
