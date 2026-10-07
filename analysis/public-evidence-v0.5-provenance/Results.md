# Public evidence provenance and feasibility audit

7 October 2026. Documentary audit only. No new package installation, scanner execution or behavioral probe was performed.

## Source audit

All 20 selected pairs carry affected[].database_specific.source links to the GitHub Advisory Database. Each linked source was retrieved at pinned revision `963f4b691a2736e0bb288f5f855915bf7ffd3c3e`, and its advisory ID and structured package ranges matched the frozen OSV record. Primary descriptive endpoint: 20/20 pairs have explicit source attribution. There were no failed source retrievals.

This is an expected result of selecting GHSA records. It does not establish independent corroboration, distinct measurement events, real affectedness or novelty. Alias linkage is distinct from copying. The identical range comparison is structural, not an evaluation of all possible semantic representations. No scanner accuracy is measured.

All 20 source modified timestamps differ from the OSV snapshot timestamps. Record-processing timestamps are not interchangeable clocks for vulnerability truth; this mismatch alone proves neither stale data nor a range change. Raw sources remain outside Git, with URLs, hashes and acquisition details in audit.json. The pinned database LICENSE.md was retrieved and hashed; original code/commit licensing requires per-case review before any adapted test is published.

| Rank | Package | Advisory | Source relationship | Ranges |
|---|---|---|---|---|
| 1 | invokeai | GHSA-227r-w5j2-6243 | Explicit GitHub source | Match |
| 2 | langroid | GHSA-22c2-9gwg-mj59 | Explicit GitHub source | Match |
| 3 | pretalx | GHSA-23fx-92m6-4f2g | Explicit GitHub source | Match |
| 4 | scrapy | GHSA-23j4-mw76-5v7h | Explicit GitHub source | Match |
| 5 | wordops | GHSA-23qq-p4gq-gc2g | Explicit GitHub source | Match |
| 6 | certifi | GHSA-248v-346w-9cwc | Explicit GitHub source | Match |
| 7 | peppol-py | GHSA-24hm-wm2h-h8w7 | Explicit GitHub source | Match |
| 8 | redis | GHSA-24wv-mv5m-xv4h | Explicit GitHub source | Match |
| 9 | apache-airflow | GHSA-2522-mrjc-m688 | Explicit GitHub source | Match |
| 10 | lightgbm | GHSA-2586-f3p4-hq84 | Explicit GitHub source | Match |
| 11 | pheonixappapi | GHSA-258h-f687-4226 | Explicit GitHub source | Match |
| 12 | whoogle-search | GHSA-2689-cw26-6cpj | Explicit GitHub source | Match |
| 13 | apache-airflow | GHSA-269x-pg5c-5xgm | Explicit GitHub source | Match |
| 14 | matrix-synapse | GHSA-26c5-ppr8-f33p | Explicit GitHub source | Match |
| 15 | gradio | GHSA-26jh-r8g2-6fpr | Explicit GitHub source | Match |
| 16 | apache-airflow | GHSA-273c-4g26-4jpm | Explicit GitHub source | Match |
| 17 | swift | GHSA-274c-rx2j-2v3x | Explicit GitHub source | Match |
| 18 | paddlepaddle | GHSA-275c-w5mq-v5m2 | Explicit GitHub source | Match |
| 19 | gradio | GHSA-279j-x4gx-hfrh | Explicit GitHub source | Match |
| 20 | pgadmin4 | GHSA-27jx-ffw8-xrqv | Explicit GitHub source | Match |

## First-six behavioral feasibility assessment

Patch diffs and PyPI release metadata were retrieved and hashed. Version pairs below are candidates with publicly listed artifacts, not downloaded/pinned installations or tested outcomes. The affected-version candidates fall within the simple intervals in the selected records. Full dependencies, environments and test licenses remain to be pinned in addenda.

| Package | Candidate versions | Assessment |
|---|---|---|
| InvokeAI | No qualifying stable fixed event | The only stated fix is 5.3.0rc1. Ineligible under the frozen stable-release rule; retain without replacement. A path-validation regression test exists, but it does not override selection rules. |
| Langroid | 0.53.14 / 0.53.15 | Plausible offline evaluation/sanitization check with benign DataFrame inputs. A sanitizer-only test would not establish protection of every agent call path. Integration and dependency feasibility pending. |
| pretalx | 2.3.1 / 2.3.2 | Plausible isolated export-path containment check. Django configuration may be required. Use disposable fixture files only; no production export. |
| Scrapy | 2.11.1 / 2.11.2 | Strong candidate for offline middleware response checks. The patch includes redirect tests; no network request is needed to observe returned request/response behavior. |
| WordOps | 3.20.0 / 3.21.0 | Conditional. Patch changes file creation to mode 0600. A mocked file-call test or extracted fragment would not establish the full race-condition claim. Requires a bounded isolated filesystem test, not system provisioning. |
| certifi | 2024.6.2 / 2024.7.4 | Strong candidate for offline certificate-store loading and membership comparison. This checks removal of GLOBALTRUST 2020, not live TLS exploitation or universal trust safety. |

The InvokeAI selector initially raised an empty-list error after filtering prereleases; recorded in feasibility.json and classified explicitly, not silently replaced. Other cases are provisionally assessable, not proven feasible. No two-hour engineering cap was exhausted, and no failed probe is being relabeled as a success.

## Next gate

Prepare per-case frozen addenda, preserving this six-case order and InvokeAI exclusion. Start with version/artifact/dependency and license pinning; define benign controls, expected outcomes and failure criteria before running. Do not expand to new advisories because a selected case is difficult. The public evidence currently supports source attribution, not improved attack-graph decisions.
