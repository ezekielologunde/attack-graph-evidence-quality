# When Verification Helps

**Failure Boundaries of Structural Remediation Decisions Under Imperfect Evidence**

Ezekiel Ologunde, Independent Researcher. Author email: ologunde@bu.edu. No corresponding-author designation.

The scoped experiments and complete manuscript are available for author review. No journal submission, acceptance, operational superiority, or new VOI algorithm is claimed.

## Paper and reproducibility

- [Complete manuscript and Overleaf package](paper/README.md)
- [Reproducibility instructions](paper/REPRODUCIBILITY.md)
- [Claim/evidence map](paper/CLAIM_EVIDENCE.md)
- [Submission status](paper/SUBMISSION_CHECKLIST.md)

## Main findings

- Frozen synthetic validation: **96 cases, 960 policy evaluations**, zero execution failures, run on ASA-X.
- Lineage/age verification versus immediate action: **27 lower-loss cases, 69 ties, zero higher-loss cases**.
- Incremental mean-loss advantage over naive verification: **0.00025**. Most gains reflect ordinary verification, not demonstrated provenance-aware superiority.
- Independence approximation harms two constructed cases: loss **2.60 to 2.78**.
- Independent rational scoring checks all 960 saved decisions, with maximum floating-point discrepancy about **1.33e-15**.
- Fixed public sample: **20 advisory/package pairs**, all with explicit GitHub source attribution. This is expected from GHSA selection, not independent corroboration.
- First-six feasibility: **four confirmed narrow checks**, **one excluded case**, **one unsupported fixture**. All 24 failed probe-container runs remain in the record, as do separate preparation failures.

[Synthetic analysis](analysis/validation-v0.4-secondary/Results.md) | [Final public results](analysis/public-evidence-final/Results.md) | [Literature positioning](protocol/manuscript-scope-and-literature-v1.md)

Run saved-evidence verification with Python 3.11 or newer:

```sh
python -m unittest discover -s tests
python src/verify_public_behavior.py
python src/verify_rational_results.py
python src/analyze_public_final.py
python src/verify_release.py
```

These commands do not execute affected packages or contact targets. Re-executing package probes needs Docker, exact external artifacts and a deliberately versioned runner configuration; see the reproducibility guide.

## Protocol and historical development

Earlier reports are chronological records. Their pending statuses are superseded by the final results above, not silently rewritten.

- [Frozen validation](protocol/validation-v0.4.json) and [ASA-X results](analysis/validation-v0.4/Results.md)
- [Public protocol](protocol/public-evidence-v0.5.md), [selection](analysis/public-evidence-v0.5-selection/Results.md), and [source audit](analysis/public-evidence-v0.5-provenance/Results.md)
- [Initial pilot](analysis/Results.md), [shared-path extension](analysis/shared-paths-v0.2/Results.md), and [integrated development model](analysis/integrated-v0.3/Results.md)
- [Requests development check](analysis/requests-behavior-v0.1/Results.md) and [scanner comparison](analysis/scanner-comparison-v0.1/Results.md)
- [Closest-work review](protocol/closest-paper-review-v0.2.md) and [full-text comparison](protocol/full-text-comparison-v0.3.md)
- [HPC handoff](hpc/README.md), [portfolio roadmap](protocol/portfolio-roadmap-2026-10-07.md), and [completion workflow](protocol/research-workflow.md)

## Rights and evidence boundaries

Original work is intentionally unlicensed pending an author decision. Third-party notices remain separate. Large raw archives, third-party wheels, tokenizer data and downloaded papers are retained outside Git; acquisition references and hashes document their identities. Public endpoints do not guarantee permanent artifact availability.

Synthetic probabilities and costs were designed, not inferred from CVSS or advisory counts. The public package checks do not calibrate graph decisions. The research contains no private participant data or live external attack targets. GitHub deposit, author approval, journal submission and acceptance are distinct states.
