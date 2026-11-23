# Homebrew sale dossier: case study

## Provenance and scope

This case study comes from James's homebrew-equipment sale dossier conversation on November 11, 2026, and the subsequent design review requested in a side conversation. Primary conversation ID: `01a1cc61-39ef-7940-a40a-deae43fb4bb2`. The design-review side conversation ID was `01a1ce27-f3a0-75e1-b296-0748e0aef269`.

The examples below preserve the reasons for design corrections without requiring access to the original chat, cached builders, photographs, or PDF. Equipment details and prices describe that historical work; they are not current inventory or valuation advice. User corrections, derived design principles, and implementation choices are distinguished below.

Read this when examples or a similar dossier would clarify a decision. Do not impose its sale workflow, reference prefixes, page format, palette, or photography layout on an unrelated artifact.

## Explicit corrections and the general lesson

| Situation in the dossier | Requested correction | Transferable lesson |
|---|---|---|
| Unphotographed components and routine checks appeared together in a parts-search list. | Separate checks from missing parts; the rod and pickup fittings were confirmed present. | Absence of a photograph is not confirmed absence of the object. Facts and actions need different roles. |
| A potentially missing part was described without a useful recognition view. | Include an actual reference photograph beside the part. | Match evidence to the task of recognizing an unfamiliar object. |
| A loose round disc was described ambiguously in a busy photograph. | James asked which piece was meant. | Identify position or provide a close-up rather than assuming a description singles out one object. |
| The working guide called James "the owner." | Use a natural reader-facing voice. | Choose perspective for the actual audience. |
| Source titles were concatenated into crowded notes. | Move genuine footnotes near the footer, one per line. | Supporting material needs an appropriate location and separate entries. |
| The revised footer still acted as an unanchored reference list. | Link notes to text, or use a named References callout explaining usefulness. | A footnote, reference block, and directory have different semantics. |
| Numerous codes appeared before the reader knew their meaning. | Explain prefixes up front; put each inventory prefix on its own row in an "Inventory items" table. | Identifiers must reduce lookup effort and have a readable key. |
| Listing IDs competed with the equipment names and pricing. | Give IDs their own pricing-table column; make them bold and smaller. | Keep lookup metadata subordinate and aligned. |
| Inline references were refined after initial sizing changes. | Use subtle pills, vertically aligned in the surrounding text; keep IDs around 80% or less of local type size. | A small metadata treatment needs optical alignment as well as numeric sizing. |
| An inch measurement read "9 in at $24.48." | Prefer the compact form `9" at $24.48`. | Use familiar notation and explicit quantity bases. |
| Preparation existed as ordinary prose. | Give each item checkable preparation bullets. | Choose a control suited to tracking the requested actions. |
| The PDF footer announced "checkboxes are interactive." | Remove the obvious instruction; the claim was also false for that PDF at the time. | Ordinary controls do not need promotional narration, and behavior must be verified in the actual format. |
| A prominent index sentence announced that controllers and the primary regulator now had separate pages. | Remove the account of an editorial decision. | Make structure evident through the structure; keep revision history outside the artifact. |
| An accounted-for block mixed contents, confirmation narration, and commands. | Rebuild it as a compact table or bullets with strong item-name emphasis. | Give the section a stable factual purpose and put actions in preparation. |
| Headings used Helvetica Bold while body text used Karla. | Make font choice deliberate and use real weights, bold, italics, and selective underlining. | Typography must carry a useful hierarchy, with actual rendered font choices verified. |
| "L01 / VERIFY BOTH UNITS" preceded the product name. | Lead with the product name; put verification in preparation. | Identity, metadata, and actions need different levels of prominence. |
| "Your equipment" and a repeated "TMP-02 Johnson Controls..." label added little context. | Remove confusing or redundant labels. | Every displayed label should help the reader identify or navigate. |
| Description, image, prices, and preparation were crowded or inefficiently stacked. | Increase vertical rhythm; use the portrait photo on the left, notes and pricing on the right, preparation below. | Compose for the material's shape and separate meaningful groups. |
| The carboy bundle was hard to follow and spilled across pages. | Call them carboys and give each constituent set a small recognizable presentation with its associated pieces. | Organize a bundle into the units its reader recognizes. |
| Photo-overlap bookkeeping received a large note. | Reduce it to a tiny endnote if needed. | Scale prominence to reader importance; internal audit notes often do not belong in the main flow. |
| Prices did not clearly state whether amounts were each or total. | Specify each, pair, kit, or bundle; give prices distinct cards and consistent labels. | A quantitative value needs its condition and quantity basis. |
| The pricing overview contained carboy-specific detail and elaborate Taprite exclusions. | Put carboy details on their own page, improve totals, and include the planned Taprite sale. | Design an overview around the comparison and scope the reader needs. |
| Reference-directory entries consumed too much space. | Consolidate into one smaller table. | Lookup material can be denser than decision and action material. |
| The old-grain discussion grew beyond the sale-page task. | Preserve the expanded answer in an appendix. | Retain useful depth with a concise main-flow implication and cross-reference. |
| The author copied an explanatory bracketed word from a request into a price label. | Omit `[untested]`; it had been an annotation for the author. | Distinguish authoring instructions from intended copy. |

## Artifact-specific compositions and choices

The PDF's fixed format was US Letter portrait, 8.5" by 11". The question about ratio did not establish that the actual page dimensions had changed. Consistent geometry was an artifact constraint, not a general default for all future output.

The useful listing-page pattern was product name, secondary listing ID, portrait photo left, description and prices right, then a preparation card and a quieter References box. The carboys used constituent picture cards. A long horizontal measuring instrument could use a different image treatment.

Three main price meanings became `as-is`, `checked`, and `sale est.`, with one main amount and quantity basis per card. Historical controller figures illustrated the distinction: $45 for the pair as-is, $80 for the checked pair, and estimated proceeds of $60–$80 for the pair. An individual-sale alternative was secondary. These labels suit that sale task; other comparisons need their own meanings.

The last request for prices "in one line" was implemented as three cards in one horizontal row with labels above values. This did not independently establish that James preferred stacked labels over a shared label/value baseline. Specify intended geometry in a future brief when that distinction matters.

James positively acknowledged Karla ExtraBold for the first-page title. Its reported 21 pt size, the palette, border colors, column proportions, and corner radii were implementation choices rather than universal preferences.

## Reconciliation examples

One black-and-blue strap group was one tall-carboy harness. The white sampling pieces formed one assembly. Bungs, airlocks, and clamps could be available without dedicated photographs. One object could appear in multiple photos. These facts needed to change associations, preparation steps, descriptions, and totals consistently rather than accumulating as isolated correction notes.

Some later revisions introduced genuinely new equipment and research. The avoidable rework came from unstable content roles, weak hierarchy, and local fixes whose effects were not checked across the artifact. A new fact should fit the existing design model; it should not require inventing a new hierarchy each time.
