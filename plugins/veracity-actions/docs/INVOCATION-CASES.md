# Invocation review cases

These are **manual instruction-review cases**, not model-executed test results. Every explicit request should currently receive a brief skeleton preview with the relevant proposed inputs, outputs and missing capabilities. It should not activate or perform the future workflow. Requests without explicit skill selection should not load these skills; that policy is declared in host metadata and repeated in each stub.

| Skill | Explicit selection to preview | Boundary / negative case |
|---|---|---|
| `focus` | Use $focus to keep this conversation directed at finishing the migration plan. | An ordinary factual question without explicit skill selection must not start a focus session. |
| `tangents` | Use $tangents to help me stay on topic while preserving useful side ideas. | A correction to the current deliverable must not be parked, and a fictional idea in a quotation must not be captured as the user’s own initiative. |
| `explore` | Use $explore for one turn on this alternative, then return to the migration plan. | Mentioning a possible alternative in passing must not begin exploration. |
| `checkpoint` | Use $checkpoint to prepare a recoverable snapshot before I leave. | A brief answer or every sentence must not trigger a checkpoint automatically. |
| `recover` | Use $recover to find where this workstream stopped and show the next action. | A user asking what happened last time must not trigger a new task, ownership transfer, or implementation. |
| `fork` | Use $fork to branch this workstream into a separate investigation. | An alternate solution mentioned in discussion must not create a fork or a new app chat. |
| `handoff` | Use $handoff to prepare this work for another conversation. | Asking for a summary must not send it to another chat or pause another writer. |
| `promote` | Use $promote to make this accepted decision part of the project’s shared context. | A speculative tangent must not become an approved project commitment merely because it was captured. |
| `memory` | Use $memory to remember this preference for future conversations. | A passing preference, sensitive aside, or useful idea without a memory request must not be saved as personal memory. |
| `assumptions` | Use $assumptions to track the premises this recommendation depends on. | A derived arithmetic result with verified inputs must not automatically create an open assumption. |
| `verify` | Use $verify to check the load-bearing claims in this proposal. | Ordinary conversation must not activate a mandatory claim-tail format without selecting this skill or a later explicit profile. |
| `decide` | Use $decide to help choose between these approaches. | A clear implementation request must not be diverted into an unsolicited decision workshop. |
| `diagnose` | Use $diagnose to investigate why this workflow is failing. | A request to explain an error message must not silently mutate the system. |
| `artifacts` | Use $artifacts to make a targeted, copy-safe update to this document. | A request for critique must not rewrite or publish the artifact. |
| `audit` | Use $audit to check this result for unsupported claims, drift, and missing recovery information. | Missing decorative glyphs alone must not block unrelated authorized work. |
| `contract-check` | Use $contract-check to inspect this contract version and its companion registry. | Mentioning Veracity or opening an old report must not fetch and apply the old operating contract. |

Review outcome: each stub has a specific trigger, defined inputs/outcomes, an explicit preview-only boundary, and a negative case. This static review does not demonstrate that a live model always obeys the instructions or that a host respects the invocation setting. Those trials remain separate from skeleton qualification.
