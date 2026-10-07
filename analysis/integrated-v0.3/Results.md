# Integrated evidence and graph development results

144 exact development calculations combine three existing graph structures, three joint priors, eight evidence patterns and two query costs. They are not 144 independent experiments. Ten policies are evaluated on each case. No public topology data or live attack outcomes are used.

The eight patterns cover one report, four correctly grouped copies, four incorrectly split copies, independent conflicting observations, falsely merged conflicting observations, correctly modeled age, underestimated age, and split copies with underestimated age. The source event and true age are evaluator-only fields. Policies receive reported labels and age. All policies know the same joint prior; the factorized comparator discards posterior dependence. This is not learning a prior from public data.

For the independent-prior bypass graph with query cost 0.25:

| Evidence | Lineage and age immediate | Lineage and age VOI | Privileged correct-model VOI |
| --- | ---: | ---: | ---: |
| Single observation | 2.50 | 2.50 | 2.50 |
| Correctly grouped copies | 2.50 | 2.50 | 2.50 |
| Incorrectly split copies | 2.50 | 2.50 | 2.50 |
| Independent conflicting reports | 2.50 | 1.75 | 1.75 |
| Falsely merged conflicting reports | 2.50 | 1.75 | 1.75 |
| Correctly modeled age | 2.50 | 1.93 | 1.93 |
| Underestimated age | 2.50 | 2.50 | 1.93 |
| Split copies and underestimated age | 2.50 | 2.50 | 1.93 |

This slice illustrates missed verification value under an incorrect age model. Duplicate-label errors alone do not change the loss in this slice. Do not turn this selected illustration into an overall effect estimate. The complete 144-case table is in results.json, including zero-benefit controls.

## Observation semantics

For each true measurement event, a binary channel has effective accuracy q(1-f)+(1-q)f, where q is sensor accuracy and f is a specified historical flip probability. This is a conditional observation model given the current gate state, not a fitted temporal network process. Separate measurement events have conditionally independent errors; copies of an event share one observation. Across-gate joint dependence resides in the prior. No empirical calibration is claimed.

Reported groups are keyed by gate and source. If rows within a reported group disagree in value, accuracy or flip probability, the grouped policy discards the entire group. This conservative design choice is order invariant and does not infer which report is correct. Inconsistent rows within a true evaluator event are invalid and raise an error. Impossible evidence also raises an error. No silent row selection is used.

All patches have unit cost and perfect efficacy; one optional query has known accuracy 0.9. Total capacity is 1.5. The privileged baseline knows correct measurement lineage and age, but not the realized state; it is a diagnostic upper-information comparator. The full-state oracle is a separate diagnostic lower loss bound.

## Verification and scope

26 tests pass, including eight added checks for duplicate invariance, a hand-calculated age posterior, independent-event Bayesian updating, conflict-order invariance, hidden-field sanitization and privileged VOI behavior. Results replay deterministically. Earlier pilot evidence remains unchanged.

A separate 96-case four-gate validation specification is sealed in protocol/validation-v0.4.json with code and fixture hashes. It is not run in this release. These are prospectively specified finite examples, not a representative public-network sample or a complete main research study. Novelty, real-data calibration, imperfect patch outcomes, uncertainty/random-query baselines and broad generalization remain unresolved.
