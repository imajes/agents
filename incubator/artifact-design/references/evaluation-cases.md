# Evaluation cases

Use these fixtures when maintaining or qualifying the skill. They are evaluation inputs and acceptance criteria, not a recorded model benchmark. Match any claims about successful behavior to an actual response or artifact that was inspected.

For implicit-selection checks, evaluate the name and description before loading the instructions. When the user explicitly invokes the skill for a narrow request, load it and preserve that narrow edit scope.

## Positive behavior

### Decision report without equipment imagery

Request: "Make a two-page A4 decision brief comparing Plan A at $600 upfront plus $50/month and Plan B at $900 upfront plus $20/month. We need a one-year choice. Use our existing Aptos-based template."

Inspect: preserve A4 and Aptos; separate upfront, recurring, and one-year amounts; compute $1,200 versus $1,140 from the supplied figures; identify the decision and evidence/assumptions; use an appropriate comparison. Do not introduce equipment cards, sale-stage labels, a prefix registry, Karla, or a portrait-photo layout.

### Workshop handout

Request: "Turn these six workshop steps into a one-page Letter handout with checkboxes and room to write observations. No photographs."

Inspect: organize around the activity sequence, leave usable writing space, keep task and supporting notes distinct, and inspect final-scale readability. Paper checkboxes need not become PDF form fields. Do not add prices, a reference directory, or a second output format solely because the skill mentions them.

### Participant roster

Request: "Lay out these eighteen names for sign-in with blank attendance and emergency-contact fields. Keep it readable on a clipboard."

Inspect: preserve all supplied names, leave unknown information blank, use a real table because row association matters, and prioritize handwriting room. Do not invent contact details, imply attendance, or force a card for each person.

### Component recognition guide

Request: "This accessory is not in the photo. I may have it in another box; help me recognize it in the kit guide."

Inspect: classify it as unresolved rather than confirmed missing; provide a recognition photograph or request a precise missing input if needed; distinguish actual and reference images, identity uncertainty, and condition checks. Do not mark a component verified simply because a similar reference picture exists.

### Narrow revision across existing formats

Request: "The missing adapter has turned up. Update the existing PDF and browser guide; keep the design."

Inspect: reconcile presence, captions, actions, descriptions, and any affected arithmetic; preserve the established design and unrelated edits; inspect changed units and downstream pagination. Do not narrate the correction in the finished guide or redesign unrelated pages.

### Evidence and identifiers

Request: "This technical guide has unexplained source codes and a footer full of links. Make the references useful."

Inspect: retain only useful identifiers, explain necessary families compactly, connect notes to text or use named supporting References blocks, and state each source's purpose. Separate entries and keep supporting material subordinate. Do not declare every link a footnote or manufacture a large identifier system.

## Negative implicit activation

| Request | Expected boundary |
|---|---|
| "Change the meeting date in this file from Friday to Saturday." | Apply the fact-only edit; no substantive design workflow. |
| "Convert this PDF to DOCX, preserving its layout." | Use format-conversion capabilities; no discretionary redesign. |
| "What is the sum of this CSV column?" | Calculate the requested result; no report or layout work unless requested. |
| "Debug this web application's checkout flow." | Use the appropriate application/UI workflow. A user interface is not a reading artifact merely because it has typography. |
| "What font is shown in this screenshot?" | Perform the focused identification; do not redesign the document. |
| "Explain what a footnote is." | Answer the ordinary chat question; do not create a durable artifact. |

## Maintenance checks

Validate skill frontmatter, UI metadata, local reference links, absence of unfinished scaffolding, and dependency statements. Check that the general entrypoint remains useful without the homebrew case study and does not require its original chat, files, photographs, fonts, or cached builders. Confirm that any new example has not silently become a universal layout or authorization rule.
