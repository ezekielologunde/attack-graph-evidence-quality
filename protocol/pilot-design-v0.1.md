# Pilot design v0.1: verify or patch?

Author: Ezekiel Ologunde, Independent Researcher. Status: proposed engineering pilot, not a registered confirmatory study. No institutional affiliation. ACM journal selection follows contribution assessment.

## Research question

Under a fixed action budget, when does paying to verify an uncertain inventory observation reduce subsequent patch-selection loss compared with immediate remediation, after controlling for duplicated sources and observation age?

## Hypotheses to test

- H1: Duplicating reports from one collection event can change naive confidence and patch ranking without adding independent information. Explicit provenance grouping should remove this duplication effect when group IDs are correct.
- H2: Verification has lower expected decision loss only when the information gained exceeds its opportunity cost. Costly checks or already decisive evidence should favor immediate patching.
- H3: Any provenance-aware benefit degrades when lineage labels are incomplete or wrong. Perfect source IDs must not be assumed in the main evaluation.

## Separate latent truth, observations and action effects

Latent state defines actual asset identity, enabled services, reachability and policy-relevant vulnerability applicability. An observation is a noisy, timestamped claim with a collector and underlying collection-event ID. Duplicates share that event; their errors are not independent Bernoulli draws. Staleness arises from explicit state changes, not an arbitrary confidence discount declared correct by construction.

Use a small exact-enumeration reference first. Patching disables a specified modeled transition, with explicit costs and possible failure. Verification returns a noisy observation with specified cost and accuracy; it is not a free oracle. Freeze the loss definition before generating comparisons. For the initial static model, use weighted critical-target reachability as an explicitly modeled loss, not real compromise probability. NASim exploit probabilities remain simulation parameters, not calibrated vulnerability probabilities.

## Comparators and fairness

1. Immediate deterministic patch ranking.
2. Naive independent-report aggregation.
3. Provenance deduplication plus immediate patching.
4. Correlation-aware belief update plus immediate patching.
5. Random verification and highest-uncertainty verification.
6. Conventional one-step expected-value-of-information acquisition followed by patching.
7. Full-state, same-budget oracle as a diagnostic ceiling, not a deployable competitor.

All applicable methods share the same decision budget, modeled action effects and observation access. Compute regret against the full-state budget-constrained action optimum on each small graph. Report both residual modeled loss and expenditure; checks consume budget. Do not give the proposed method true hidden source IDs while denying that metadata to a baseline meant to use it.

## Initial cases and tests

Build inspectable development cases: no uncertainty; independent disagreement; duplicated one-source reports; stale service identity; conflicting collectors; and incorrect provenance labels. Include a case where verification is worth its cost and one where it is not. No sample-size claim is attached to these engineering cases. Verify exact oracle optima, probability normalization, budget accounting, duplicate invariance and no access to latent truth by deployable policies.

For subsequent evaluation, split entire topology families and state-change generators, not rows or corrupted replicas. Fix policies and parameters on development cases, then freeze code, hypotheses, exclusions and a held-out schedule. Size that study after pilot variance and meaningful effect requirements are known. Repeated policies on the same scenario are paired observations, not independent samples.

## Data and limitations

Three upstream NASim scenario fixtures and their license are pinned in data/raw/nasim. They provide reusable topology/service configurations, not patch interventions, correlated scanner evidence, or remediation outcome labels. A documented adapter and independently checked decision-loss model are still needed. Do not describe the simulator as a validated production digital twin. Do not redistribute classroom topology files without confirming rights.

Primary outcomes: paired intervention regret, residual modeled loss, budget spent, unnecessary patches and critical targets left reachable. Secondary: calibration only where probabilities have declared meaning, runtime, and sensitivity to verification cost, error rate and source-label corruption.

Stop or revise if the loss is circularly defined to favor the proposed policy, verification is effectively an oracle, or the result disappears against ordinary deduplication/VOI. Negative findings remain reportable.
