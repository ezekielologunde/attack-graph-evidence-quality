# First-six probe preparation register

7 October 2026. Package artifact identities are pinned in public-evidence-v0.5-artifacts.json. Ten universal wheels were downloaded from PyPI and their SHA-256 values verified against release metadata. No wheels were installed or package behavior executed. Wheel metadata was read as data. Optional dependency declarations are included in raw Requires-Dist lists; declaration counts are not installed dependency counts.

## Ordered case disposition

1. **InvokeAI:** excluded under the frozen stable fixed-event rule; only 5.3.0rc1 is specified. No substitute case or later stable version is selected.
2. **Langroid 0.53.14 / 0.53.15:** top-level artifacts pinned. Draft observable: benign DataFrame calculation succeeds, while an expression rejected by the patched sanitizer is rejected through the actual compute_from_docs path. No shell commands or dangerous payloads. Must pin compatible pandas and transitive dependencies, identify a minimal real invocation and review any borrowed test license. Status: environment/addendum incomplete; no execution authorized by this specification.
3. **pretalx 2.3.1 / 2.3.2:** top-level artifacts pinned. Draft observable: export-path traversal is rejected while ordinary in-root output succeeds, using disposable filesystem fixtures. Must pin Django and transitive dependencies and determine how to invoke the real export function with minimal settings. Do not equate a reimplemented path check with package behavior. Status: environment/addendum incomplete.
4. **Scrapy 2.11.1 / 2.11.2:** top-level artifacts pinned. Draft observable: actual redirect middleware accepts an ordinary HTTP redirect, but does not return a request for a non-HTTP redirect in the patched release. No downloader or live network. Must resolve and freeze common compatible dependencies, including Twisted and cryptography-related packages; document both middleware paths and original test authorship/license if reused. Status: environment/addendum incomplete.
5. **WordOps 3.20.0 / 3.21.0:** top-level artifacts pinned. Draft observable: initial permissions of a newly created synthetic configuration file. Must use a disposable container and fixture path, never /etc or system provisioning. A mocked call or extracted snippet cannot establish a reproduced race; if real code cannot be exercised within two hours, record infeasible. Transitive dependencies and fixture injection remain unresolved. Status: environment/addendum incomplete.
6. **certifi 2024.6.2 / 2024.7.4:** ready specification below. Reaching this preparation entry does not replace or declare completion of cases 2-5. Execute the first-six sequence only after their disposition is explicitly recorded.

## Certifi frozen behavioral specification

Advisory GHSA-248v-346w-9cwc, CVE-2024-39689. Selected interval starts at 2021.5.30 and fixes at 2024.7.4. The greatest preceding stable release found in the recorded PyPI metadata is 2024.6.2. Both exact wheel filenames, URLs and hashes are in the artifact manifest. There are no declared runtime dependencies.

Environment: Linux container image python@sha256:2d97f6910b16bd338d3060f261f53f144965f755599aab1acda1e13cf1731b1b, Python 3.9. Use Python standard-library zipfile, ssl, hashlib, resource, time and json. Do not install either wheel. Load the original wheel's certifi/cacert.pem bytes into a fresh SSLContext with no default operating-system CA paths. Enumerate binary trusted certificates with get_ca_certs(binary_form=True), then compute SHA-256 fingerprints. This exercises the SSL trust-store loading behavior of the supplied bundle; it does not invoke certifi's Python API or establish end-to-end TLS behavior.

Target certificate fingerprint, documented in upstream removal commit bd8153872e9c6fc98f4023df9c2deaffea2fa463: 9a296a5182d1d451a2e37f439b74daafa267523329f90f9a0d2007c334e23c9a.

Expected observation: this target fingerprint appears in the old bundle's loaded trust store and is absent from the fixed bundle's store. Control: both contexts load successfully and contain at least one common non-target certificate fingerprint. Negative/no-trigger control: a fresh context without loaded CA data contains neither the target nor any bundle certificates. Record all fingerprints/counts for both bundles, without private certificates or keys.

Isolation and limits: Docker --network none, --read-only, --cap-drop ALL, --security-opt no-new-privileges, one CPU, 512 MB RAM, at most 64 processes, disposable tmpfs only, read-only wheel/probe mounts. No Docker socket or full home-directory mounts. External watchdog: 30 seconds per repetition. Three repetitions, each in a fresh container, report repeatability and runtime variation only.

Outcome rules: confirmed narrow change only if all expected observations and controls pass in all three repetitions; contradicted if validly loaded stores fail the expected version distinction; inconclusive for inconsistent repetitions; environment failure for missing artifacts, hash mismatch, context/import/loading errors or timeout. Never relabel environment failure as an unaffected version. Retain every stdout/stderr record and exit code.

Record acquisition time from the artifact ledger separately from container startup/setup and in-container probe time. Capture resource.getrusage peak RSS (KiB on Linux) and process CPU time; do not call it whole-container peak memory. Record image digest, probe code hash, wheel hashes and exit status for each repetition. Freeze probe implementation hash in a run manifest before its first execution. Two-hour engineering limit applies.

Licensing and origin: a new original probe will be written; no upstream regression-test code is copied. Certifi wheel LICENSE files identify MPL 2.0 terms; preserve notices if distributing its bundle, and keep downloaded wheels outside Git. The advisory and removal commit informed the target fingerprint and expected change. This is not independent discovery and not proof of universal trust safety.

## Remaining preparation gate

Cases 2-5 need exact transitive locks and completed per-case addenda before execution. The top-level artifact manifest is not a complete environment lock. Preserve frozen v0.5 and v0.4 files. If implementations require scope changes, record an amendment before running. No outcome has been collected at this stage.
