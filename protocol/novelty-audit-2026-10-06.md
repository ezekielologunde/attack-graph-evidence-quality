# Initial novelty audit

6 October 2026. Focused scoping pass, not a systematic review or proof of priority. No experiments or effectiveness results yet.

| Primary source | Access in this pass | Overlap and consequence |
| --- | --- | --- |
| [Nguyen et al., uncertainty in network security analysis](https://publish.illinois.edu/science-of-security-lablet/files/2014/05/An-Approach-to-Incorporating-Uncertainty-in-Network-Security-Analysis-1.pdf) | PDF initially retrieved by browser; targeted follow-up failed. Detailed comparison pending. | Historical portfolio identifies uncertain connectivity and vulnerability applicability. Do not claim probabilistic attack graphs or correlation handling as new; recheck exact assumptions before asserting an omission. |
| [Progressive attack graph, 2025](https://link.springer.com/article/10.1007/s10207-025-01125-w) | Publisher introduction and model inspected | StatAG/SteerAG address progressive generation and query-directed analysis. Graph updating and incomplete graph analysis are already active research areas. Our proposed endpoint is patch-choice loss under imperfect observations, not generation speed. |
| [Optimal Value of Information in Graphical Models](https://arxiv.org/abs/1401.3474) | Abstract-level record | Value-of-information selection is established. A verify-before-patch policy must be compared with a conventional expected-value-of-information baseline, not only immediate patching. |
| [Uncertainty for Active Learning on Graphs, ICML 2024](https://www.cs.cit.tum.de/daml/graph-active-learning/) | Authors' abstract and official code description | Uncertainty acquisition on graphs already has principled baselines and pitfalls. Node-label acquisition is not the same endpoint as remediation, but uncertainty sampling is an essential comparator. |
| [Mapping Evidence Graphs to Attack Graphs](https://www.nist.gov/publications/mapping-evidence-graphs-attack-graphs) | NIST publication record | Connecting evidence and attack graphs predates this proposal. Evidence provenance alone is not a novelty claim. |
| [CAPG-v2 lead, 2026](https://www.scitepress.org/publishedPapers/2026/150641/pdf/index.html) | Indexed publisher excerpt only; direct full-text requests failed | Excerpt describes graph-aware patch prioritization and probabilistic semantics. Treat as a potentially close competitor; no gap claim against the inaccessible paper. |

## Candidate contribution

A reproducible intervention benchmark that separates the number of reports from the number of independent observations, charges verification against the same budget as patching, and measures realized patch-selection regret under duplicate, stale and conflicting evidence. This is our proposed comparison, not a gap demonstrated absent from all prior work.

## Decision

Proceed to a small measurement-feasibility pilot, not a claimed new algorithm. Before a larger study, resolve CAPG-v2, read the uncertainty paper in full, and inspect the ProgressiveAttackGraph artifact. Expand the search to security investment, adaptive sensing, source dependence, and cost-sensitive diagnosis. If conventional deduplication plus expected value of information solves the constructed cases, report that result and narrow the contribution to the benchmark.

Queries used included attack graph observation provenance correlated evidence value of information patch prioritization; 2025 2026 attack graph uncertainty vulnerability verification remediation prioritization; attack graph value of information; and attack graph active learning uncertainty remediation. No exhaustive search or citation coverage is claimed.
