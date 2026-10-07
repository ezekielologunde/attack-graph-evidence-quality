# Shared advisory provenance feasibility result

The first acquisition gate passes narrowly: source lineage is explicit for one advisory, and two downloadable package artifacts have checkable identities. This does not yet validate a research benchmark or a novelty claim.

| Check | Result | Interpretation |
| --- | --- | --- |
| Advisory identity | Both identify GHSA-j8r2-6x86-q33q | Same advisory, not two independent discoveries |
| Declared source | OSV points to GitHub Advisory Database | Direct evidence of upstream reuse for this record |
| Version ranges | Both specify introduced 2.3.0, fixed 2.31.0 | Agreement in an inherited claim |
| Full comparison projection | Different | OSV adds PYSEC-2023-74 and a package URL; raw inequality does not imply an independent observation |
| Requests 2.30.0 wheel | Metadata identity and PyPI SHA256 match | Artifact identity independently checked; advisory lists this version affected |
| Requests 2.31.0 wheel | Metadata identity and PyPI SHA256 match | Artifact identity independently checked; advisory identifies the fixed boundary |

Affectedness remains advisory-derived. Absence from a version list alone is not proof of safety; the explicit fixed boundary is the relevant advisory claim. A fixed version for this CVE does not mean a package has no other vulnerabilities.

No scanner was run and no local behavior test, deployed inventory check, patch action or operational loss measurement occurred. Acquisition latency was recorded once per endpoint and cannot stand in for verification-policy cost. This deliberate example cannot estimate how often shared provenance occurs.

## Decision

Keep the direction for a second feasibility gate. Build an independent local behavior check for a narrowly defined affected behavior, with a vulnerable and fixed artifact plus negative controls. Pin dependencies, prohibit external test traffic and distinguish behavior coverage from complete exploitability. Then inspect actual scanner outputs and their database lineage before choosing a comparison policy. Do not count the current advisory lookup as that second gate.

If the behavior oracle cannot be defined independently, narrow the endpoint to artifact/version identification and reassess whether the resulting contribution is meaningful. The planned 96-case synthetic validation is unchanged and remains unexecuted.
