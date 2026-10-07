# Two scanner feasibility comparison

7 October 2026. OSV-Scanner 2.6.0 and Trivy 0.75.0 scanned the same two synthetic requirements.txt inputs declaring Requests 2.30.0 and 2.31.0. Images were pinned by digest. Read-only input mounts contained only the synthetic manifests; no host repository, Docker socket, credentials or installed application was exposed to either scanner. Temporary Trivy cache was removed after preserving its metadata and database hash. Scanner images remain locally available.

| Declared version | OSV focal CVE | Trivy focal CVE | Earlier offline API check |
| --- | --- | --- | --- |
| 2.30.0 | Present | Present | HTTPS proxy header present with credentials |
| 2.31.0 | Absent | Absent | HTTPS proxy header absent |

The focal CVE is CVE-2023-32681. Other vulnerabilities were reported in both versions and are retained in raw output; their behavior was not adjudicated. Absence of this CVE is not a general safety result.

## Evidence lineage

OSV's affected-version output includes GHSA-j8r2-6x86-q33q, whose source points to GitHub Advisory Database, and PYSEC-2023-74, whose source points to PyPA's advisory database. These are grouped aliases for the focal vulnerability, not independent discoveries. Trivy identifies its focal finding's data source as GitHub Security Advisory pip. Its primary display link points to Aqua's CVE page; a display link is not the same as the advisory ingestion source.

There is therefore an observable shared GitHub advisory source between the scanners for this finding. This does not prove their entire pipelines are identical or that the PyPA record is an independent measurement. Two agreeing scanner results should not be counted as two independent behavioral confirmations. The earlier local API observation provides a different evidence type, but checks only header construction, not complete exploitability.

## Execution and limits

All four scans produced valid JSON and identified the requested package/version. OSV returned exit code 1 with findings; Trivy returned 0 with findings under its default exit behavior. Exit-code differences do not imply scanner disagreement. Trivy warned that no site-packages directory was available for license detection; this test intentionally scans manifests and does not inspect installed artifacts.

OSV used online advisory queries; its raw returned vulnerability records are preserved. Trivy used one freshly acquired database across its two scans; database metadata and SHA256 were captured, but the database itself is not redistributed. Image pinning plus a database hash does not guarantee future reproduction of the same live database. Offline reanalysis of saved outputs is supported with `python src/analyze_scanner_comparison.py`.

Acquisition and scan wall times include differing cache and network conditions, especially Trivy's initial database download. They are not comparative performance or operational verification-cost measurements. This deliberate one-CVE, two-version case has no statistical generalization claim, no measured policy benefit and no established novelty. Public upstream advisory content embedded in tool outputs retains its original source attribution; it is not original research prose.

## Next research gate

The feasibility chain now connects manifests, actual scanner findings, visible upstream provenance and a narrow local behavioral check. The next study must add independently selected cases and configurations where information can actually change an action, including discordant scanners and unknown provenance. Freeze selection criteria and outcomes before collection. Do not expand only around examples that favor source-aware verification. The 96-case graph validation remains a separate, unexecuted plan.
