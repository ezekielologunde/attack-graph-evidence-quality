# Manuscript claim and evidence map

| Manuscript statement | Evidence | Boundary |
|---|---|---|
| 96 cases and 960 policy rows | analysis/validation-v0.4/cases.jsonl and run.json | Finite designed grid |
| Primary counts 27 lower, 69 ties, zero higher | analysis/validation-v0.4-secondary/analysis.json | Paired cases, tolerance 1e-9 |
| Incremental mean benefit 0.00025 | Secondary all-policy aggregates and case comparisons | Does not establish broad provenance advantage |
| Dependence harms 2.60 to 2.78 in two cases | Saved factorized decisions, secondary analysis, rational-audit/results.json | Constructed related cases, not prevalence |
| Universal cut and budget threshold | Frozen graphs and action constraints; elementary proofs in paper | Structural loss only |
| Rational audit matches 960 scores | src/verify_rational_results.py and analysis/rational-audit/results.json | Saved decisions scored independently; same workflow |
| 20/20 explicit source relationships and matching ranges | analysis/public-evidence-v0.5-provenance/audit.json | Expected GHSA sample property, not independence |
| Four confirmed narrow public cases | analysis/public-evidence-final/verified-results.json and linked raw logs | No full exploit or operational outcomes |
| 24 retained setup failures | Original Scrapy and Langroid run series | Additional preparation failures counted separately |
| Novel algorithm / improved real remediation | No supporting evidence | Explicitly not claimed |

Review main.tex against these artifacts before author approval. Earlier pending-status reports are historical snapshots; final public dispositions are in analysis/public-evidence-final/Results.md.
