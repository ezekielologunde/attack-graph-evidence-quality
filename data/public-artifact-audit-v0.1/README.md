# Public artifact feasibility snapshot

This snapshot covers GHSA-j8r2-6x86-q33q / CVE-2023-32681 and Requests wheel versions 2.30.0 and 2.31.0. Selection was deliberate: a documented patch boundary and machine-readable source lineage. It is not a random or representative sample.

The GitHub advisory was retrieved at commit `161aa622af11e0b687366ff64cf068f7cca59a50`. The OSV response declares that GitHub record as its upstream and enriches it with an additional alias, package URL and version listing. Original response bytes are preserved. Acquisition URLs, timestamps, SHA256 hashes and byte lengths are in audit.json.

Attribution: GitHub Advisory Database contributors, [upstream record](https://github.com/github/advisory-database/blob/161aa622af11e0b687366ff64cf068f7cca59a50/advisories/github-reviewed/2023/05/GHSA-j8r2-6x86-q33q/GHSA-j8r2-6x86-q33q.json), licensed CC BY 4.0; retained in UPSTREAM-LICENSE.md. OSV is the service supplying the enriched upstream advisory representation. Its raw response is identified separately and must not be mistaken for an unchanged GitHub file. Original analysis code remains unlicensed under the repository policy.

PyPI wheel files were downloaded into memory and read as ZIP archives without installation or code execution. Their hashes matched PyPI's published digests. Only derived identity facts and hashes are saved; wheel contents and PyPI metadata responses are not mirrored. These downloaded artifact identities do not establish what is installed on any operational system.

Reacquire into a new directory with `python src/public_artifact_audit.py --output NEW_DIRECTORY`. This is a current-data acquisition, not a promise of byte-identical historical replay. The script refuses to overwrite an existing directory. Use `python src/analyze_public_audit.py` for offline replay of this fixed snapshot.
