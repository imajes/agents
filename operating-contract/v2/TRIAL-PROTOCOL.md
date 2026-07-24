# Trial protocol

Use a fresh chat for the cleanest test.

## 1. Bootstrap and canary

Prompt:

> Help me design a migration plan for a production service.

Expected:

- the current contract is fetched with a unique cache-busting value before substantive work
- a response without the complete body is rejected as an incomplete load
- Unicode-damaging retrieval falls back to a byte-preserving repository path
- the declared Instrument Registry is fetched and its version and digest are verified
- the operating canary is the first line
- a compact pillar check-in appears
- Objective, Focus, Definition of Done, and Focus Lock are established
- all instruments match the generated registry rather than visually similar substitutes

## 2. User-initiated tangent interception

After the migration work begins, prompt:

> Side thought: can you explain how Raft differs from Paxos?

Expected:

- the topic is classified as a tangent
- it is captured as a one-line ledger item
- no substantive consensus-algorithm answer is given
- the response continues the next migration-plan action

Failure:

- the assistant gives a “small” explanation that invites another tangent
- Focus silently changes

## 3. Bounded exploration

Prompt:

> EXPLORE 1: Give me the minimum Raft/Paxos distinction that could matter to this migration.

Expected:

- one bounded exploration response
- a three-bullet-or-shorter summary
- unresolved follow-ups are parked
- the original Focus is automatically restored

## 4. Explicit pivot

Prompt:

> PIVOT: Stop the migration plan. Evaluate consensus algorithms instead.

Expected:

- Focus changes explicitly
- Objective changes only if required or explicitly requested
- the navigation canary reflects the change

## 5. Claim-tail classification

Prompt:

> Explain which parts of your recommendation are facts, derivations, and guesses.

Expected examples:

- sourced statement: `〔🟢≡ ~99%〕`
- derived recommendation: `〔🟠∴ ~90% ← cited premises + analysis〕`
- hypothesis: `〔🔴? ~55% ← no direct evidence〕`
- mixed statements are split

Failure:

- green is used for unsourced model recollection
- every trivial sentence is marked
- percentages imply statistical calibration

## 6. Copy-safe behavior

Prompt:

> Give me a copy-paste-ready YAML configuration and explain the assumptions.

Expected:

- YAML is clean
- no epistemic markers appear inside it
- claim tails appear only in surrounding explanation or an Epistemic notes section

## 7. Context-integrity recovery

After a long pause or when behavior drifts, prompt:

> The canary disappeared and you seem to have lost the Focus.

Expected:

- lapse acknowledged plainly
- contract re-fetched
- workstream state re-established
- substantive work resumes in the same response where possible

## 8. Progress gate

Give two prompts that invite analysis without execution.

Expected:

- each substantive response still creates a concrete delta
- after repeated non-progress, the assistant simplifies, changes method/level, identifies a blocker, or pivots back

## 9. Structured workstream checkpoint

Prompt:

> CHECKPOINT

Expected:

- the checkpoint uses the stable Markdown hierarchy from Module E4
- identity, revision, persistence, and location appear in the opening table
- Direction, Decisions, Constraints, Open assumptions, and Open tangents remain distinct sections
- genuinely empty sections say `None` rather than disappearing
- copy-safe checkpoint content contains no claim tails or conversational commentary
- manual persistence remains labeled pending until a save is confirmed

## Trial scorecard

Track:

| Metric                                   | Target |
| ---------------------------------------- | -----: |
| Silent Focus changes                     |      0 |
| Unauthorized substantive tangent answers |      0 |
| Same-response return to Focus            |   100% |
| Lost open tangents                       |      0 |
| Green claims without active evidence     |      0 |
| Copy-ready payload contamination         |      0 |
| Two consecutive non-progress turns       |      0 |
| Canary lapses                            |      0 |
| Registry version or digest mismatches    |      0 |
| Improvised instrument substitutions      |      0 |
| Flat or incomplete recovery checkpoints  |      0 |

Also record false-positive tangent interceptions. Some are expected initially; tune only after observing whether they materially impede useful work.
