# Provenance-aware attack-graph decisions

[Public-evidence protocol v0.5](protocol/public-evidence-v0.5.md): contribution narrowed to failure boundaries and a bounded public-artifact audit. Fixed screening and probe gates specified; new collection has not started.

[Validation secondary analysis](analysis/validation-v0.4-secondary/Results.md): all ten policies compared; gains largely reflect verification rather than lineage correction, two dependence-approximation harms identified, and numerical query ties disclosed. Reproduce with `python -B src/analyze_validation.py`.

[Portfolio roadmap and current-project completion checklist](protocol/portfolio-roadmap-2026-10-07.md): finish this attack-graph study before starting the next AI cybersecurity project.

[ASA-X CPU handoff](hpc/README.md): preflight confirmed express queue limits and system Python 3.9.21. CPU smoke job 97283 and frozen validation job 97288 completed on ASA-X. GPU execution remains unverified.

[Actual scanner comparison](analysis/scanner-comparison-v0.1/Results.md): OSV-Scanner and Trivy agree on the focal CVE across two manifest versions and expose a shared GitHub advisory source. Raw output and offline comparison code are preserved; no accuracy or performance ranking is claimed.

[Offline behavior feasibility check](analysis/requests-behavior-v0.1/Results.md): 16 API-level cases distinguish Requests 2.30.0 and 2.31.0 header handling without sending requests. This is a narrow behavioral oracle, not an end-to-end exploit or scanner benchmark.

[Public-artifact feasibility audit](analysis/public-artifact-audit-v0.1/Results.md): one shared advisory lineage and two Requests wheel identities verified. Subsequent scanner and narrow offline behavior checks are linked above; broad independent affectedness labels and operational costs remain unmeasured.

[Alternative directions and selection, 7 October 2026](protocol/alternative-directions-2026-10-07.md): six candidate pivots compared. Preferred next step is a public-artifact feasibility audit of shared advisory provenance and decision-relevant verification; novelty remains provisional.

**Latest:** [integrated evidence model v0.3](analysis/integrated-v0.3/Results.md) evaluates 144 designed cases; 26 tests pass. Run `python src/evidence_graph.py`. A [96-case prospective validation grid](protocol/validation-v0.4.json) completed on ASA-X: 96 cases and 960 policy rows, with no execution failures. See [validation results](analysis/validation-v0.4/Results.md). This finite model validation is not the main empirical study.

**Status: exact synthetic feasibility pilot completed.** Three public NASim scenario fixtures are pinned with their license and hashes. Nine designed model cases have been evaluated by exact enumeration. No live experiments, validated novelty, production outcome dataset, or final paper are claimed.

**Dependency extension v0.2:** 18 additional designed calculations cover three shared-path graphs, three joint state distributions and two verification costs. [Results and limitations](analysis/shared-paths-v0.2/Results.md). These are development cases, not held-out validation. All 18 unit tests pass. Run `python src/shared_paths.py` to regenerate the versioned results and hash manifest. The original nine-case pilot remains unchanged.

- [Initial novelty audit](protocol/novelty-audit-2026-10-06.md)
- [Closest-paper comparison and study gates](protocol/closest-paper-review-v0.2.md): broad novelty claims rejected; a narrower evidence-lineage benchmark remains provisional.
- [Full-text supplement](protocol/full-text-comparison-v0.3.md): Nguyen and CAPG-v2 methods inspected; structural reachability and finite-horizon attacker loss require separate evaluation. Broader novelty clearance and CAPG evaluator access remain open.
- [Pilot design v0.1](protocol/pilot-design-v0.1.md)
- [Data provenance](data/README.md)

[Research protocol and prior-art leads](protocol/research-plan.md). This plan comes from the October 4, 2026 independent research portfolio. Its literature assessment must be refreshed before implementation and submission.

## Research identity and publication route

Author: **Ezekiel Ologunde**. Affiliation: **Independent Researcher**, with no institutional affiliation. Corresponding email is pending confirmation. Intended route: a suitable ACM journal, selected after assessing the completed contribution. No journal has accepted this work and no publisher metadata or DOI is assigned.

## Repository workflow

Keep research questions and hypotheses in `protocol/`; put code in `src/`, tests in `tests/`, and analyses in `analysis/`. Store redistributable datasets with provenance in `data/`, including source URL, retrieval date, version, license, SHA-256, schema, and role in the study. For restricted or large data, publish an acquisition script and manifest instead of copying files. Never commit credentials, private participant records, or copyrighted downloaded papers.

Freeze each experimental plan and code revision before collection. Retain failed and excluded runs with reasons. Publish analysis and result artifacts as work progresses. Keep manuscript drafts in `paper/`, clearly versioned; deposit the author-permitted final paper after journal-policy review. A planned experiment is not a result, and public code is not peer-reviewed acceptance.

Original work is intentionally unlicensed pending an author decision. Preserve applicable third-party notices. No dataset or final paper is claimed to exist merely because its directory is present.

## Synthetic pilot

[Results](analysis/Results.md) | [Implementation and limitations](protocol/pilot-implementation-notes.md) | [Case definitions](data/pilot-cases.json)

Run with Python 3.11 or newer, standard library only:

```sh
python -m unittest discover -s tests
python src/pilot.py
```

The pilot uses a two-path synthetic graph, not the NASim fixtures. Standard VOI improves the constructed cheap-verification case from 4.0 to 2.5 expected modeled loss, but correctly skips verification when expensive. Source-label errors defeat the provenance correction. These are analytical model expectations, not empirical attack frequencies. Original work remains unlicensed.
