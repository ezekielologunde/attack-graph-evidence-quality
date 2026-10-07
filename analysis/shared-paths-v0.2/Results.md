# Shared-path development model v0.2

This exploratory extension contains 18 exact calculations: three graph structures, three joint state distributions and two verification costs. There are no sampled attack trials, independent replications, held-out cases or empirical confidence intervals. NASim fixtures are not used.

## Findings

The shared-gateway and parallel-route graphs each have an affordable single patch that cuts every path. All four policies attain zero modeled loss across their 12 cases and decline optional verification. This negative control matters: uncertainty alone does not make verification useful.

For the bypass graph, expected terminal loss is:

| Joint distribution | Query cost | Joint immediate | Factorized immediate | Joint VOI | Factorized VOI |
| --- | ---: | ---: | ---: | ---: | ---: |
| Independent | 0.25 | 2.500 | 2.500 | 1.750 | 1.750 |
| Independent | 0.75 | 2.500 | 2.500 | 2.500 | 2.500 |
| Common cause | 0.25 | 4.250 | 4.250 | 4.125 | 4.125 |
| Common cause | 0.75 | 4.250 | 4.250 | 4.250 | 4.250 |
| Exclusive enabling | 0.25 | 0.000 | 0.000 | 0.000 | 0.300 |
| Exclusive enabling | 0.75 | 0.000 | 0.000 | 0.000 | 0.000 |

In the exclusive-enabling case, only one gate can be enabled. Immediate patching of the bypass gate prevents all target reachability. A factorized belief wrongly assigns probability to simultaneous enabling, buys a noisy check, and sometimes selects the wrong patch. Its expected loss rises to 0.3. This is a constructed counterexample to assuming that an optional information-gathering policy cannot hurt under model misspecification. It is not a new algorithm or an established literature gap.

## Model and boundaries

Each graph uses three latent binary gates and eight enumerated states. A gate may enable multiple edges. Reachability counts each target once, including when several paths reach it. Patching a gate removes every edge controlled by it. Unit patch costs and perfect efficacy are assumptions. The shared budget is 1.5; query costs are 0.25 or 0.75; query accuracy is 0.9. At most one gate can be queried. Query errors are conditionally independent given the true state. Higher query cost leaves insufficient capacity for any patch.

Joint policies receive a correctly specified distribution, not the realized state. Factorized policies receive its identical one-gate marginals but assume independence. Both have the same graph, costs and sensor accuracy. The evaluator uses the joint distribution to score decisions; a separate full-state oracle supplies a diagnostic lower bound. This comparison presumes known dependence and does not demonstrate learning dependence from data. The label common cause describes a chosen positively dependent distribution; no causal mechanism is estimated.

This extension isolates graph and state dependence. It does not integrate the original pilot's source duplication, historical state flips or incorrect lineage labels. It therefore cannot establish a provenance-aware benefit on shared graphs. It supplements, rather than supersedes, the original evidence-quality pilot.

## Verification and next study gate

Eight new unit tests bring the total to 18. Hand-derived Boolean formulas independently check all eight states and all eight patch subsets for each graph, 192 comparisons. Further checks cover correlated updates, marginal factorization, shared cuts, branch-level budgets, oracle bounds, cycles, invalid probabilities and impossible query branches. Deterministic replay and preservation of the original pilot manifest are checked before publication.

Before a main study: resolve the closest-paper comparison; integrate source dependence and observation age with these graph semantics; freeze development and held-out topology families plus parameter ranges before generating test results; include misspecified dependence and imperfect patch outcomes. These 18 cases must remain development examples and must not be relabeled as held-out evidence. Report per-topology paired comparisons without pooling policy views as independent observations.
