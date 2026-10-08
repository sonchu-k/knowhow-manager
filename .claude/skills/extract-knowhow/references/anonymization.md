# Handling identifying information

This file covers how to remove proper nouns and identifiers. That is only the minimum. After removing them, the event still has to be lifted to a principle and rewritten; see [conceptualization.md](conceptualization.md) for that.

## What to remove

| Kind | Examples | How to replace |
|---|---|---|
| Personal names, nicknames, IDs | Full names, employee numbers, account names | Describe the role ("the decision-maker on the client side", "a newly appointed lead") |
| Contact details | Email, phone, address, social accounts | Delete |
| Company and organization names | Own company, clients, suppliers, competitors | Describe position and nature ("the manufacturer placing the order", "a large competitor") |
| Product, service, project names | Internal code names, unreleased product names | Describe the type ("an internal request system") |
| Amounts and contract terms | Quotes, unit prices, contract periods | Use order of magnitude or ratio, or delete |
| Dates and periods | Specific dates | Use relative terms ("two weeks before release", "start of the fiscal year") |
| Places | Site names, store names, municipalities | Delete, or reduce to something like "a regional office" |
| Internal information | Unpublished strategy, personnel matters, sales figures, incident details | Delete if the know-how does not need it. If it does, keep only the structure |
| Sensitive personal information | Health, family, evaluations, beliefs | Delete |
| System identifiers | URLs, host names, IPs, ticket numbers, file paths | Delete |

The names of publicly available tools and methods (widely used software, frameworks, methodologies) may stay when they are themselves the content of the know-how. Avoid wording that ties them to which company uses them.

## Identification by combination

Details that are harmless one by one can identify when listed together.

> At a long-established sake brewer in Hokuriku with about 300 employees, when the core system was replaced in spring 2025…

No company name, yet people involved can almost certainly tell. Keep only the attributes the know-how depends on.

> When replacing a core system at a mid-sized manufacturer that has used the same one for many years…

Decide what to keep by asking "would the know-how stop holding if this attribute changed?" If it would still hold, the attribute is unnecessary; drop it.

## Structure and wording are clues too

Even with every proper noun gone, the following let someone who knows the source, or who searches on wording, find where it came from.

- Lists with the same item names, classification names, or ordering as the source
- Coined terms or unusual phrases particular to the source
- Numbers and procedural details that have nothing to do with the principle
- Paraphrases that keep the original word order
- Paragraphs narrating what happened
- Tags, categories, or `source_type` values that put back context removed from the body
- Events that can be reconstructed by reading several know-how items from the same document side by side

These are removed by rewriting from the principle, not by substitution.

## Example of generalizing

**Original (fictional)**

> Director Yamada at Company A balked the moment he saw the price in the first proposal, but when Tanaka brought three plans side by side to the second meeting, they agreed on the middle one at 12 million yen straight away.

**Bad: names hidden, nothing else**

> A director at a certain company balked at the first proposal, but when three plans were presented side by side the second time, they agreed on the middle one at 12 million yen.

Still a record of an event, the amount is still there, and it does not tell the reader what to do next time.

**Bad: generalized too far**

> It is important to make proposals from the other party's point of view.

Could be written without the source, and changes nobody's behavior.

**Good**

> Presenting a single quote turns the other party's decision into "accept or refuse", so resistance to the price tends to become refusal. Presenting several options of differing scope side by side turns the decision into "which one", and agreement comes more easily. It also works as a way to recover after a first quote has met resistance on price.

Nobody can tell whose story it is, but what to do and why it works are still there.

## When in doubt

- If you are unsure whether to keep a specific detail, drop it.
- If the know-how no longer holds without it, do not save that know-how; ask the user to decide.
- If the whole document is sensitive (personnel evaluations, a dispute whose parties are obvious), check with the user before starting to extract.
