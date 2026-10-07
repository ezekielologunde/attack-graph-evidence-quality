# Public evidence v0.5 selection

Selection completed 7 October 2026. No new scanner or behavioral probes have run.

The official current OSV PyPI snapshot contains 26,104 records: 1,521 eligible records yield 1,600 unique advisory/package pairs. The fixed lexicographic rule selects 20 pairs. The remaining 24,583 records are excluded; exclusion reasons overlap. No parser failures were recorded. An independent replay confirmed the selected pairs and output hashes.

The 20 selected entries have no shared IDs/aliases connecting them within this sample. This does not prove independent discovery, independent source evidence, or absence of relationships outside the sample.

Archive SHA-256: `d26cf9bf4f8bc878d0cdde1d115503cd78c5fce0629ff9840b9cdf6d9801019b`.

The full archive stays outside Git. selection.json records acquisition headers, retrieval UTC, source/code/protocol hashes, selected member hashes and fixed-version candidates. screening-ledger.jsonl accounts for every record. Source licenses and behavioral feasibility have not yet been audited. These are identifiers and screening metadata, not republished full advisory texts.

| Rank | Advisory | Package | Probe feasibility stage |
|---|---|---|---|
| 1 | GHSA-227r-w5j2-6243 | invokeai | First six, assessment pending |
| 2 | GHSA-22c2-9gwg-mj59 | langroid | First six, assessment pending |
| 3 | GHSA-23fx-92m6-4f2g | pretalx | First six, assessment pending |
| 4 | GHSA-23j4-mw76-5v7h | scrapy | First six, assessment pending |
| 5 | GHSA-23qq-p4gq-gc2g | wordops | First six, assessment pending |
| 6 | GHSA-248v-346w-9cwc | certifi | First six, assessment pending |
| 7 | GHSA-24hm-wm2h-h8w7 | peppol-py | Not selected for probes |
| 8 | GHSA-24wv-mv5m-xv4h | redis | Not selected for probes |
| 9 | GHSA-2522-mrjc-m688 | apache-airflow | Not selected for probes |
| 10 | GHSA-2586-f3p4-hq84 | lightgbm | Not selected for probes |
| 11 | GHSA-258h-f687-4226 | pheonixappapi | Not selected for probes |
| 12 | GHSA-2689-cw26-6cpj | whoogle-search | Not selected for probes |
| 13 | GHSA-269x-pg5c-5xgm | apache-airflow | Not selected for probes |
| 14 | GHSA-26c5-ppr8-f33p | matrix-synapse | Not selected for probes |
| 15 | GHSA-26jh-r8g2-6fpr | gradio | Not selected for probes |
| 16 | GHSA-273c-4g26-4jpm | apache-airflow | Not selected for probes |
| 17 | GHSA-274c-rx2j-2v3x | swift | Not selected for probes |
| 18 | GHSA-275c-w5mq-v5m2 | paddlepaddle | Not selected for probes |
| 19 | GHSA-279j-x4gx-hfrh | gradio | Not selected for probes |
| 20 | GHSA-27jx-ffw8-xrqv | pgadmin4 | Not selected for probes |

Next: source-provenance audit for all 20 pairs, followed by per-case frozen addenda before any behavior checks. Fixed release candidates are metadata, not independently confirmed remediation outcomes.
