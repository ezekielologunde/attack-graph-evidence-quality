# Closest paper comparison and research decision

Review date: 6 October 2026. Author: Ezekiel Ologunde, Independent Researcher.

**Decision: retain this as a candidate benchmark study, not a novel algorithm.** The pilots establish calculational feasibility. They do not establish a literature gap. Correlated uncertain graphs, dependency-aware patch ranking, budgeted information gathering and defense under partial observability all have prior work. A larger confirmatory study is not yet frozen.

## Comparison register

Access labels describe what was actually inspected. An unmentioned feature is not proof that a paper omits it. Author-stated future work is separated from our proposed research question.

| Source and access | Established overlap | Implication and remaining comparison |
| --- | --- | --- |
| Nguyen, Palani and Nicol, 2017, [An approach to incorporating uncertainty in network security analysis](https://experts.illinois.edu/en/publications/an-approach-to-incorporating-uncertainty-in-network-security-anal/). Institutional abstract and indexed author PDF abstract; direct PDF timed out. | Models uncertain connections and vulnerability existence, including correlations caused by common underlying factors. | Correlated gate states in our v0.2 cannot be claimed new. Full model and evaluation comparison remains open. The 2018 thesis lead was retrieved but its relevant passages were not successfully inspected, so it does not close this item. |
| Krause and Guestrin, [Optimal Value of Information in Graphical Models](https://arxiv.org/pdf/1401.3474). Full-text sections 4.1 and 4.2 inspected. | Observation selection and conditional plans account for costs, budgets and outcomes. | Our one-query expected-loss calculation is a conventional VOI baseline. These algorithms have specific graphical-model assumptions; do not claim their implementation is a drop-in attack-graph comparator. |
| [Progressive attack graph](https://link.springer.com/article/10.1007/s10207-025-01125-w), 2025. Publisher model and limitations inspected; linked artifact README and directory metadata inspected. | StatAG and SteerAG support progressive generation and query-directed analysis. Authors identify logical-graph extensions, threshold setting and steering-model improvements as future work. | Those are author-stated directions, but do not directly establish our evidence-lineage gap. Partial computational enumeration differs from uncertain real network facts. Use the artifact as a candidate topology source, not verified patch-outcome ground truth. |
| Issa, Gruska and Ali, [CAPG-v2](https://www.scitepress.org/publishedPapers/2026/150641/pdf/index.html), 2026. Publisher-indexed title, abstract and introduction only; direct retrieval returned 403/error. | Impact-weighted, overlapping-path vulnerability prioritization; Monte Carlo marginal expected-loss reduction; JSON artifacts and reference evaluator announced. | Very close to our weighted reachability and patch-removal semantics. No claim that its model ignores dependence, sensing, or provenance is supported yet. Artifact URL and full methods remain unresolved. |
| Jiang et al., [VulRG](https://arxiv.org/html/2502.11143v1), 2025 preprint version. HTML framework overview and conclusion inspected. | Communication and dependency graphs support contextual risk propagation and patch ranking. Authors propose future real-time threat intelligence, predictive models and broader sector evaluation. | Graph context and dependency-aware prioritization are established. Their stated future work does not prove absence of faulty-lineage evaluation. Need detailed scoring and data comparison before implementing a numerical baseline. |
| [SmartPatch](https://www.sciencedirect.com/science/article/pii/S0166361521002025), 2022. Publisher abstract and highlights only. | Cost-constrained patch strategy with architectural and patch dependencies and multiple attack avenues. | Budget constraints and patch interdependence are not new. Full-text sensing and observation-model coverage remains unknown. |
| [CyGATE](https://arxiv.org/html/2508.00478v1), 2025 preprint version. Introduction, model overview and knowledge-base description inspected. | Partially observable attacker-defender simulation, belief states and Bayesian dependencies; NVD and CISA-derived knowledge base. | Partial observability and belief-based defense are established. Knowledge-base size and simulated performance are author reports, not independently reproduced evidence. Inspect its observation/action definitions before asserting a verification-budget gap. |
| [Partially-Observable Security Games for Automating Attack-Defense Analysis](https://arxiv.org/abs/2211.01508), 2022. Abstract record only. | Further prior-art lead for attack-defense analysis with imperfect observation. | Expand comparison into security games and active diagnosis. Abstract-level access cannot establish a missing feature. |

## Narrow candidate question

Under a shared verification-and-patching budget, how do wrong source-group labels and stale observations change patch-selection regret on graphs with shared dependencies, relative to immediate patching and standard VOI?

This is our inferred candidate question. None of the reviewed author-stated future-work passages specifically establishes this combined gap. A combination of familiar features is not sufficient novelty by itself. The potential contribution is a reproducible, decision-relevant stress test showing when common evidence assumptions change intervention choices.

## Hypotheses for a later frozen protocol

1. Correct source grouping makes decisions invariant to pure copies of the same observation. This is principally an implementation property, not an empirical discovery.
2. Incorrect grouping and misspecified dependence can make model-selected verification worse than immediate patching under the evaluator distribution. The v0.2 counterexample motivates measuring the extent of this effect; its existence is not claimed novel.
3. Verification benefit varies with decision relevance and remaining patch capacity. Graphs with an affordable universal cut are a required negative control, not cases to exclude for lack of improvement.

Primary endpoint: paired difference in expected residual target loss between a verification policy and its immediate-patch counterpart under the same evaluator distribution and total budget. Report query rate, branch-level budget feasibility and same-budget oracle regret. A correctly specified joint model is a privileged-model diagnostic comparator, not an operationally available method unless its parameters can be estimated from allowed training data.

## Public data suitability

The [ProgressiveAttackGraph artifact](https://github.com/XAIber-lab/ProgressiveAttackGraph) reports an anonymized 246-host use case with vulnerabilities and reachability. GitHub API inspection pinned revision `cc6fddb3114e434199d3b0f676fc79cf7ec7647e` and identified `use_case_data/anonymized_network.json` at 4,430,457 bytes. The README identifies an MIT license, which still needs content-level review before copying data. No dataset was downloaded or executed in this pass. The README does not establish scanner lineage, observation-age distributions, verification accuracy or intervention outcomes.

Previously pinned NASim fixtures remain useful simulated topology candidates, with the same missing observational and patch-outcome calibration. Public CVE severity and exploited-vulnerability catalogs must not be converted into gate-success probabilities without a justified measurement model. If source dependence and age are generated synthetically, label them as designed stressors and keep real topology provenance separate from synthetic observations.

## Required work before confirmatory collection

- Obtain CAPG-v2 methods and evaluator, and Nguyen's full uncertainty model. Resolve their treatment of shared causes and expected-loss intervention semantics. Record an access failure as unknown, never as feature absence.
- Compare security-game and active-diagnosis observation/action costs, including CyGATE and the 2022 security-games lead.
- Integrate original source-lineage and age semantics with v0.2 graph dependence. Current pilots test these separately.
- Inspect and pin a public topology artifact, its schema and license; document every topology-to-gate mapping assumption.
- Freeze topology families, parameter ranges, training/calibration rules, baseline implementations and analysis before generating held-out cases. Keep all existing 27 designed calculations in development only. Shared policy outputs are paired, not independent trials.
- Include incorrect lineage, dependence misspecification, imperfect patch efficacy and no-benefit controls. Preserve negative results. If established baselines cover the question and the benchmark adds no useful evidence, narrow or stop the novelty claim.

## Search record and limits

Focused searches covered attack-graph uncertainty and correlation, graph-aware patch prioritization, value of information, CAPG-v2, budgeted cyber sensing and partially observable defense. Primary publisher, author, institutional and artifact pages were used. This is a targeted comparison, not a systematic review, exhaustive citation search or proof of priority. Searches for CAPG-v2 implementation and full-text assumptions produced unrelated results as well; those were excluded. No copyrighted full papers were copied into this repository.
