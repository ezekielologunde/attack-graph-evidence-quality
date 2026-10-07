# Secondary analysis of frozen validation v0.4

Analysis date: 7 October 2026. This is post hoc descriptive analysis of existing outputs, not a new validation run or a prospectively specified subgroup hypothesis test. Run `python -B src/analyze_validation.py` to regenerate the machine-readable analysis, all-policy table and analysis manifest. No frozen model or protocol was modified.

## Integrity and scope

Verified the original output manifest and sealed source/input hashes, all 96 unique cases, all 960 policy rows, saved primary summaries, budget constraints and oracle-regret arithmetic. The original protocol uses tolerance 1e-9 for outcome comparisons. Aggregates below weight each designed case equally; they are not estimates for a real-world case distribution. Cases reuse graphs and evidence patterns and are not independent empirical observations.

See [all ten policies](policy-table.md) and [complete paired comparisons](analysis.json). The privileged policy knows the correct observation model; it does not know the realized gate state. The perfect-state oracle is a separate lower bound.

## Why verification helped or tied

The lineage_age policy lowered modeled loss in 27 cases, tied in 69 and increased loss in none. It selected a query in 29 cases, including two numerical ties with no change in patch choice.

| Condition | Cases | Lower loss | Tie | Higher loss |
|---|---:|---:|---:|---:|
| Query cost 0.25 | 48 | 27 | 21 | 0 |
| Query cost 0.75 | 48 | 0 | 48 | 0 |
| Independent prior | 48 | 16 | 32 | 0 |
| Shared-cause mixture | 48 | 11 | 37 | 0 |
| Diamond graph | 32 | 16 | 16 | 0 |
| Shared bridge | 32 | 0 | 32 | 0 |
| Bypass cycle | 32 | 11 | 21 | 0 |

**Budget mechanism:** total budget is 1.5 and each patch costs one. A query costing 0.25 leaves enough for a patch; one costing 0.75 leaves only 0.75, so no patch is affordable after querying. There is no direct benefit for information without a patch in this one-step objective. This explains the expensive-query ties. It is a discrete budget threshold, not broad empirical evidence about verification pricing. Query cost is a budget constraint, not an additive penalty in the loss objective.

**Topology mechanism:** in the shared-bridge graph, patching gate 0 cuts access from the entry to every target. Immediate action already has zero loss, so verification cannot improve it. Diamond and bypass graphs sometimes require choosing between competing patches; a cheap informative query can change the branch-dependent action.

## Does provenance correction itself drive the result?

The finite-grid mean immediate loss is 1.865833 for every policy family. Mean VOI losses are 1.701417 for naive and deduplicated policies, 1.701167 for lineage_age, 1.704667 for factorized_lineage_age, and 1.700667 for the privileged policy.

Thus most of the headline gain is verification versus immediate action, not an established advantage of provenance correction. Deduplication alone produces no loss improvement over naive verification on this grid. The lineage_age improvement over naive verification is only 0.00025 in mean loss: a material difference in one case (0.024 divided by 96), apart from roundoff. That case is the shared-cause bypass graph with correctly reported staleness and cheap querying: loss changes from 2.12 to 2.096.

The lineage_age policy drops conflicting groups in 12 cases, but a dropped group is not evidence of improved decisions. False source splitting still causes repeated reports to be counted as distinct sources. Underestimated staleness remains a model error. This validation does not justify a claim that lineage correction broadly improves remediation.

## A concrete dependence failure

In two shared-cause bypass cases, with evidence patterns `single` and `copies_correct` and query cost 0.25, the factorized policy queries gate 3 and chooses gate 0 or gate 2 for patching depending on the answer. Its true expected loss is 2.78, versus 2.60 for immediate patching of gate 2, a deterioration of 0.18. The joint lineage_age policy stays with immediate action. Treating gate dependence as independent can therefore make apparently useful verification harmful in these constructed cases.

## Numerical decision caveat

In `copies_split` and `split_and_stale` for the shared-cause bypass graph at cost 0.25, lineage_age queries gate 0 but patches gate 2 for either answer. Loss ties immediate action within 1e-9 while spend rises from 1 to 1.25. The frozen planner compares floating-point expected risks without a tie tolerance. Algebraically equivalent choices can therefore select a redundant query because of rounding. The naive policy also selects such a redundant query in `copies_correct`; deduplication removes it without changing loss.

Do not silently fix this in the sealed run. Preserve the decisions and costs. Any future numerical tie-handling change requires a versioned amendment and separate results. The current outcome-count tolerance does not make the underlying planner numerically tolerant.

## Claims supported and outstanding evidence

| Claim | Assessment | What is still needed |
|---|---|---|
| Cheap verification can improve structural-loss decisions | Supported for specified synthetic cases | Operational costs and independently measured consequences for deployment claims |
| Dependence approximation can harm verification | Two explicit constructed counterexamples | Broader prespecified graph/distribution study before frequency claims |
| Provenance correction materially improves real remediation | Not established | Multiple independent public advisory lineages, meaningful disagreement, independent behavior checks and decision costs |
| Expensive verification is generally unhelpful | Not established | Budgets and costs spanning patch-feasibility thresholds; clearly separate budget effects from information value |
| Public scanner agreement means independent corroboration | Not supported | Trace upstream sources and assess actual independence |
| These findings establish novelty | Not established by this analysis | Updated closest-work comparison with a narrowly stated contribution |

## Next study gate

First decide whether the bounded contribution should center on dependence failures, evidence lineage, or their interaction. Audit available public cases before selecting outcomes. A prospective extension should specify eligible package/advisory pairs, source provenance, exact behavior probes, negative controls, exclusions, independent units, measured verification costs and the mapping from observations to decisions. Do not infer gate probabilities or network topology directly from scanner labels. Preserve uncertain labels as uncertain.

The existing one-advisory Requests feasibility check is too narrow to establish operational generalization. If suitable public cases cannot support the intended empirical claim, narrow the paper to a transparent synthetic methods/case study and explain the limits. The current analysis is ready for the evidence audit; the overall project is not yet submission-ready.
