# Provenance-aware attack-graph decisions

Status: Proposed. Historical candidate design, not a preregistration or proven novelty claim. Source: independent research portfolio dated 2026-10-04.

**Research question:** At a fixed budget, when does checking an uncertain observation reduce expected loss more than acting on the current patch ranking?

**Existing coverage:** [Nguyen, Palani and Nicol, HoTSoS 2017](https://publish.illinois.edu/science-of-security-lablet/files/2014/05/An-Approach-to-Incorporating-Uncertainty-in-Network-Security-Analysis-1.pdf) already model uncertain connectivity, vulnerability presence, and correlated edge existence. [NIST risk aggregation work](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=926022) also addresses correlation. A probabilistic graph or correlated-edge model is therefore not the contribution.

**Proposed difference:** Connect observation provenance and age to actual intervention regret in a released benchmark. Duplicate collectors may repeat one underlying source; three agreeing strings are not three independent witnesses. Preserve the distinction between asset identity uncertainty, vulnerability applicability uncertainty, and attack-success probability.

**Build and experiment:** Use the 26-device ground truth as one synthetic development scenario, then generate separately held-out topologies. Inject stale identities, duplicate observations, missing firmware and conflicting evidence using registered corruption rates. Compare deterministic ranking, independent-probability ranking, a correlation-aware baseline, and a policy that can request another observation. Charge every check and patch against the same budget. Compare against an oracle with the complete scenario state.

**Metrics:** Intervention regret, top-k action agreement, unnecessary patches, missed reachable critical assets, calibration and runtime. Do not turn ATT&CK links or KEV membership into per-edge success probabilities. Release provenance schemas and perturbation seeds, subject to course-material rights.

**Stop or narrow:** If a standard correlation-aware baseline solves the problem, the contribution may be a reproducibility dataset rather than a new algorithm. One classroom topology cannot establish generalization.
