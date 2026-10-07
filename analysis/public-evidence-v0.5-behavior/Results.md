# Public behavior checks v0.5

These are narrow offline package checks, not end-to-end exploit or operational remediation experiments. The original probe and execution addendum were committed before execution. Corrections are separately versioned; original failed runs are retained.

## Case dispositions

| Case | Status |
|---|---|
| InvokeAI | Excluded by frozen stable fixed-event criterion; no replacement |
| Langroid | Environment-blocked: wheel-only resolution could not satisfy halo>=0.0.31 |
| pretalx | Environment-blocked: wheel-only resolution could not obtain csscompressor~=0.9.0 |
| Scrapy | Six successful corrected runs; both middleware checks and HTTPS controls pass |
| WordOps | Environment-blocked: wheel-only resolution could not obtain pynginxconfig |
| certifi | Three successful repetitions; target trust-anchor distinction and both controls pass |

The environment blockers are not proof that installation is impossible. Source builds and historical dependency compatibility remain unfinished work. The two-hour per-case engineering limit has not been exhausted. No blocked case is counted as a behavioral negative or positive.

## Certifi

Loading the 2024.6.2 bundle into a fresh SSLContext includes the GLOBALTRUST 2020 fingerprint; loading 2024.7.4 does not. All three repetitions satisfy the common non-target certificate and empty-context controls. No default OS trust store, network request or live TLS handshake was used. This validates the narrow bundle-loading difference, not a universal trust-safety claim.

## Scrapy setup history

Six original runs failed before probing because the temporary filesystem prohibited executing virtual-environment tools. After a pre-execution setup amendment, six runs failed importing Scrapy because the resolved w3lib lacked a required internal symbol. A further amendment pins w3lib 2.2.1 in both environments, retaining the original probe. The corrected environments differ in Scrapy itself and an additional defusedxml 0.7.1 dependency for the fixed release; all shared wheel hashes are preserved in the lock.

The probe passes synthetic HTTPS and file-URI redirect responses to real Location and MetaRefresh middleware. It never follows returned requests or reads a target file. Repeated runs are repeatability checks, not independent vulnerability samples. stdout, stderr, pip check/freeze, hashes, image identity, UTC, total elapsed time and in-process timing/RSS are retained. Total container elapsed minus probe elapsed approximates setup/teardown overhead, not isolated installation time.

## Remaining research

Finish source-build environment preparation for Langroid, pretalx and WordOps under separate exact locks and completed addenda. This report does not close their feasibility work. Keep these observations separate from synthetic attack-graph losses: no empirical gate probabilities, query-error rates or patch costs were estimated.

## Verified Scrapy outcomes

| Middleware input | 2.11.1 returns redirect Request | 2.11.2 returns redirect Request |
|---|---|---|
| Location, HTTPS control | Yes, 3/3 | Yes, 3/3 |
| Location, file URI | Yes, 3/3 | No, 3/3 |
| MetaRefresh, HTTPS control | Yes, 3/3 | Yes, 3/3 |
| MetaRefresh, file URI | Yes, 3/3 | No, 3/3 |

All returned URLs match the predefined expectations. This establishes the specified middleware behavior in the pinned environments, not successful file access or an end-to-end exploit. Across the six selected advisory cases, two narrow behavioral checks are complete, three remain environment-blocked, and one is excluded. These counts are not population success rates.

Run `python src/verify_public_behavior.py` to verify saved outcomes and the evidence manifest without executing affected packages. The manifest covers raw outputs, environment receipts, relevant protocol files, and execution and verification scripts. It detects file changes but is not a cryptographic signature or proof of collection time.
