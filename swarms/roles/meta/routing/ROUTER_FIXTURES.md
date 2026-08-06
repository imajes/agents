# Agent task router fixtures

Status: proposed forward-test cases for the future routing skill. They do not authorize delegation or execution. The [router specification](ROUTER_SPEC.md), [live manifest](../ROLE_MANIFEST.md), and [AGT-011](../DECISIONS.md#agt-011--the-future-router-is-recommendation-only) define the current contract.

Each fixture states the expected routing shape and key exclusions, not exact prose. A candidate router should be judged on ownership, boundaries, authority gates, and dependency shape.

## Citation-backed support assistant

Input: “Our document-heavy support assistant needs current, citation-backed answers from private product documentation.”

Expected:

- `ai_architect` owns the architecture decision and evaluation plan.
- `researcher` may characterize source freshness and citation requirements; `security_engineer` covers data boundaries; `data_analyst` helps with evaluation design when needed.
- Implementation is a later staged `programmer` or `machine_learning_engineer` handoff after the architecture decision.
- Do not assume vector RAG; compare direct context, keyword/hybrid retrieval, structured sources, and vector retrieval.

## Production latency and recovery

Input: “Cut p95 latency and MTTR for our production API.”

Expected:

- `reliability_engineer` is primary for SLOs, telemetry, incident/recovery analysis, capacity, and reliability plan.
- `programmer` owns code remediation; `security_engineer` joins only for a material security control or risk.
- Production changes are an explicit authority gate.

## Fraud classifier

Input: “Train and ship a fraud classifier from our labeled transaction data.”

Expected:

- `machine_learning_engineer` owns the dataset/model/evaluation/inference artifact.
- `data_analyst` may validate definitions and population shifts; `security_engineer` covers sensitive data and abuse risk.
- `ai_architect` is support only if platform/provider/integration shape remains materially open; `reliability_engineer` joins for production serving readiness.
- Paid training, external upload, and production deployment are separate gates.

## Customer onboarding and renewal

Input: “Improve onboarding and renewals for SMB customers.”

Expected:

- `customer_success` owns the post-sale success journey, health/risk model requirements, and playbooks.
- `data_analyst` supplies adoption/retention evidence; `product_manager` receives product gaps; `marketer` owns lifecycle campaign strategy only where commercial messaging is needed; `navigator` sequences an accepted cross-team remedy when one is required.
- Customer contact, CRM edits, discounts, and contract promises require exact authority.

## Rust CI dependency conflict

Input: “Fix this Rust CI dependency conflict.”

Expected:

- `machinist` is the single primary for dependency/toolchain/CI diagnosis.
- Add `programmer` only if the resolution requires owned source changes.
- Exclude `reliability_engineer`: this is development machinery, not production reliability.

## Graph-backed assistant decision

Input: “Assess whether we should launch a graph-backed assistant for cross-document entity relationships.”

Expected:

- `ai_architect` is primary; `researcher`, `critic`, and `security_engineer` may provide distinct evidence or gates.
- Require proof that multi-hop relationship/provenance queries justify graph construction and maintenance.
- If current evidence cannot decide, `ai_architect` proposes a bounded decision-owner-approved experiment, `programmer` or `machine_learning_engineer` executes only that experiment, and the result returns to `ai_architect` for the final recommendation.
- Do not add an implementation agent before the architecture decision is accepted except to execute such a decision-owner-approved bounded experiment; full implementation waits for the accepted architecture.

## Patch review

Input: “Review this API patch for regressions.”

Expected:

- `reviewer` is the single primary.
- Add `validator` only when a reusable harness or validation gap is part of the task.
- Exclude `critic` unless a separate non-code design decision is explicitly under challenge.

## Material ambiguity

Input: “Make our AI better.”

Expected:

- `clarify-first` or `analyst` because success criteria, user outcome, system, evidence, and authority are materially unknown.
- Do not default to `ai_architect`, `machine_learning_engineer`, or a swarm merely because the prompt says AI.
