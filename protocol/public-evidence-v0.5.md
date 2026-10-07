# Public evidence feasibility protocol v0.5

Specified 7 October 2026, before new collection. Status: screening protocol ready; no new records collected or probes executed. This is a bounded descriptive study, not a confirmatory test of operational remediation effectiveness. The existing Requests case is development evidence and excluded from new-case counts.

## Contribution decision

Working title: **When Verification Helps: Failure Boundaries of Structural Remediation Decisions Under Imperfect Evidence**.

The proposed contribution is a reproducible characterization of decision failures and no-benefit conditions, supported by a public-artifact audit of the observation assumptions. It is not a new VOI algorithm, uncertainty formalism, or proven provenance-aware improvement. The current grid shows only a 0.00025 mean-loss advantage of lineage_age over naive verification; most gains are ordinary verification. Two dependence-approximation harms and budget thresholds are more informative than a broad superiority claim.

RQ1 (existing synthetic results): under the specified graph and observation models, when does query-then-patch improve or worsen structural loss relative to immediate patching?

RQ2 (new public evidence): what source relationships and independently executable behavioral checks can be established for a fixed, transparently selected set of public package advisories?

Keep these evidence streams separate. Public source relationships motivate stressors; they do not calibrate latent gate distributions, query accuracy, patch efficacy or target losses. Scanner agreement is neither independence nor ground truth. Shared vulnerability identifiers, explicit downstream relationships and copying of a measurement event are different concepts.

## Stage A: fixed screening procedure

1. Acquire the official OSV PyPI ecosystem archive from https://storage.googleapis.com/osv-vulnerabilities/PyPI/all.zip once. Save retrieval UTC, URL, byte count, SHA-256, HTTP metadata where available, and the unmodified archive outside Git. If retrieval fails, log and retry the same endpoint; do not substitute an unrecorded mirror. The archive is a current snapshot, not an as-of historical database.
2. Parse records without executing package code. Eligible records have an ID beginning GHSA-, an affected PyPI package, a published timestamp from 2023-01-01 through 2025-12-31 UTC, and at least one explicit fixed version event. Exclude withdrawn records and the development advisory GHSA-j8r2-6x86-q33q. Log exclusions and counts. Preserve unknown or invalid fields as screening failures.
3. Sort by advisory ID, then PEP 503 normalized package name. Collapse duplicate advisory/package pairs. Select the first 20 pairs, or all if fewer exist. This is a deterministic convenience sample, not a random or representative sample. Do not replace pairs based on disagreement, apparent novelty, probe availability or results. Retain shared aliases as links, not independent samples.
4. Freeze a manifest of selected IDs, package names, snapshot hashes and selection-code revision before inspecting scanner outputs or running behavior checks. Alias-linked entries are reported in clusters; do not count source records or package versions as independent vulnerabilities.
5. Retrieve each selected advisory from its original public source where identifiable, plus linked OSV/PyPA records as needed to trace provenance. Save URLs, timestamps, hashes, source revision and license. A missing source remains missing, never assumed independent. Current mutable sources are not automatically synchronized; flag snapshot-time mismatches.

No broad ecosystem dump or copyrighted article is committed to Git. Publish selected redistributable records with required notices; otherwise publish acquisition references and hashes.

## Stage B: provenance audit, all selected pairs

For each pair record: advisory and alias IDs, package identity, affected/fixed intervals, published/modified/withdrawn fields, explicit source links, references, licenses, retrieval status and analyst notes. Classify each relationship as explicit ingestion/copy, explicit upstream/downstream relationship, shared reference only, or unresolved. Classification requires cited fields or source documentation. Identical wording alone does not prove a common measurement event; different database names do not prove independence.

Compare normalized affected-version assertions only after confirming package and version semantics. Record agreement, disagreement, unknown, and not-comparable separately. Do not treat all disagreement as database error. Report all selected pairs and alias clusters with complete denominators, including missing records.

Primary descriptive endpoint: number of selected pairs with at least one explicitly traceable source relationship, out of all selected pairs. Secondary outputs: unresolved relationships, comparable range agreement/disagreement, retrieval failures and probe feasibility. No p-values, population confidence intervals or precision/recall against advisory labels.

## Stage C: behavioral feasibility, maximum six pairs

Assess the first six selected pairs in the same fixed order, regardless of outcome. Do not replace infeasible pairs. For each, check whether a public regression test or documented local behavior can distinguish an affected from fixed version using a bounded isolated test. Static metadata, descriptions and scanner labels alone are not behavioral truth.

Choose the lowest stable fixed release identified by a valid advisory interval for which artifacts are publicly retrievable. Choose the greatest stable release below it that the same interval marks affected. Use PEP 440 ordering; if intervals are incomparable or package selection remains ambiguous, record not feasible instead of choosing a favorable pair. Pin exact package/dependency artifacts and hashes before execution.

Before any probe, commit a per-case addendum containing: exact versions and dependencies; environment; source and license of any adapted test; observed property; expected outcomes; benign/no-trigger control; timeout and resource cap; artifact identities; and criteria for confirmed, contradicted, inconclusive and environment failure. Freeze a maximum engineering effort of two hours per case; report infeasibility when exceeded. Do not run unknown package installation hooks outside isolation.

Run only local isolated fixtures with no external targets or real credentials. Prefer offline function-level tests. An unsupported or unsafe fixture is an explicit limitation. A probe checks the stated behavior, not the absence of every vulnerability in a fixed package. Advisory-informed test design is disclosed; it is a distinct observation channel, not statistically independent discovery. Retain contradictory and inconclusive outcomes.

Record acquisition/setup time separately from probe wall time and peak resource use. Three execution repetitions assess repeatability/runtime variation, not three independent vulnerability samples. Do not convert those timings into an operational patch cost or calibrated query-error probability.

## Scanner extension gate

The existing OSV-Scanner/Trivy comparison is development evidence. Before extending it to the new sample, specify tool image digests, command lines, database snapshot identifiers, package manifests, network requirements and handling of normal vulnerability exit codes. Freeze these in a separate addendum before running scanners. If a database snapshot cannot be retained, disclose reproducibility limits. Scanner agreement is descriptive only, and is not used to choose the sample.

## Hypotheses and limits

H1 is a feasibility expectation: some multi-source records will have explicit shared provenance. It is not a novel assertion; OSV documents aggregation. H2 is a feasibility expectation: some selected pairs permit a repeatable local behavioral check. Neither expectation establishes a remediation improvement.

The current dependency counterexamples support a bounded synthetic claim. Any claim that measured source relationships improve graph decisions requires a separately justified observation model and a prospectively specified decision experiment. Do not invent deployment topology or numerical priors from CVSS, record counts or timestamps.

No v0.4 reruns, numerical tie fixes, new synthetic parameters or model tuning are part of this protocol. A subsequent numerical amendment must retain original outcomes and evaluate the changed planner separately.

## Deliverables and stopping rules

- Snapshot and selection manifest, complete exclusion ledger, and a table for every selected pair.
- Provenance classifications with field-level supporting evidence and explicit unknowns.
- Up to six frozen probe addenda and result records, including infeasible cases.
- A claim/evidence matrix distinguishing synthetic, documentary and behavioral support.
- A final go/no-go decision for empirical expansion. If all relationships are unresolved or no probes are feasible, report the result and narrow the manuscript; do not search until favorable examples appear.

The sample size is an effort-bounded feasibility choice, not a power calculation. Unknowns are not negative labels. No empirical outcomes have been gathered under v0.5 yet.

## Sources and novelty status

OSV aggregation and public exports: https://google.github.io/osv.dev/data/

OSV quality guidance distinguishes package-level information and leaves some validation questions out of scope: https://google.github.io/osv.dev/data_quality.html

Previously inspected close methods and semantic differences remain documented in full-text-comparison-v0.3.md. Further leads checked at abstract level on 7 October 2026: https://arxiv.org/abs/2211.01508 and https://arxiv.org/abs/2508.00478. Neither abstract establishes absence of a feature. Full-method comparison against active diagnosis and partially observable security games is still required before a novelty claim.

This protocol is versioned in Git and locally hash-sealed before collection. That is not external preregistration or proof of priority.
