# Offline Requests header behavior check

7 October 2026. Two pinned Requests wheels were tested without installation. Each was imported in a separate isolated Python worker with the same pinned dependencies. Acquisition used PyPI; workers blocked socket connection, DNS, binding and sendto audit events. No HTTP request was sent. Credentials and hostnames were synthetic.

The worker prepares a request and calls Session.rebuild_proxies directly. It observes whether Proxy-Authorization is present afterward. Each row below was tested both with and without a preexisting synthetic header, for 16 checks total.

| Destination | Proxy credentials | Requests 2.30.0 header | Requests 2.31.0 header |
| --- | --- | --- | --- |
| HTTP | Absent | Absent | Absent |
| HTTPS | Absent | Absent | Absent |
| HTTP | Present | Present | Present |
| HTTPS | Present | Present | Absent |

All 16 outcomes matched the specified expectations. Negative controls and the HTTP positive control distinguish the narrow change from simply removing every proxy authorization header. These are deterministic API cases, not independent statistical replications.

## Evidence meaning

Header presence was measured by executing package code, independently of advisory range lookup. Case selection and expected behavior were informed by the advisory and upstream regression-test pattern, so this is not independent discovery. It establishes a narrow behavioral oracle, not end-to-end exploitation, actual credential disclosure, deployment affectedness, complete patch correctness or measured remediation benefit.

This is a feasibility improvement over version identity alone. It does not yet show that consulting a second scanner improves an intervention decision or that the research direction is novel. Real scanner outputs and source-database lineage are still needed before a scanner comparison.

## Reproduction and provenance

Run `python src/run_requests_behavior.py` from a fresh checkout without the existing result artifact, or use the worker with the recorded wheel set. The acquisition runner refuses to overwrite results. Results contain exact wheel URLs, SHA256 hashes, retrieval times and dependency versions. Downloaded wheel digests were checked against PyPI metadata. Wheels were temporary, removed after execution, and are not redistributed. The manifest hashes scripts and results.

Dependencies were urllib3 1.26.18, idna 3.10, certifi 2024.8.30 and charset-normalizer 2.0.12. These define this experiment, not a recommended deployment environment. Per-call timings are single measurements and are not operational verification-cost estimates.

One development attempt failed before behavior measurement because replacing socket.socket broke library initialization. The final worker uses Python audit hooks instead. No failed attempt was counted as a successful case. No held-out or prospective validation claim is made. The separate 96-case graph validation remains unexecuted.
