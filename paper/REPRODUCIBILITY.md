# Reproduce and inspect the study

Author: Ezekiel Ologunde, Independent Researcher. Email: ologunde@bu.edu. No corresponding-author designation. Original work remains unlicensed.

## Start with saved evidence

Use Python 3.11 or newer for the local verification scripts. No network, GPU or third-party Python package is needed for this sequence from the repository root:

```sh
python -m unittest discover -s tests
python src/verify_public_behavior.py
python src/verify_rational_results.py
python src/analyze_public_final.py
```

The unit suite has 26 tests. The independent rational audit checks all 96 cases and 960 saved policy rows. Public verifiers check the final Langroid, pretalx, Scrapy and certifi observations, controls, case counts and retained setup failures. The first public verifier additionally checks its historical evidence manifest. Final release hashes are checked with `python src/verify_release.py`.

`src/analyze_validation.py` regenerates the earlier post hoc descriptive tables. It verifies frozen source/output hashes before analysis. No verification script reruns an exploit, contacts a research target, or changes the frozen synthetic planner.

## Re-execution is a different operation

The frozen v0.4 calculation uses `hpc/validate.py` and the protocol under `protocol/validation-v0.4.json`; consult the HPC README and runner arguments before launching. Its original output is preserved under `analysis/validation-v0.4`. Do not overwrite it. The reported ASA-X run used Python 3.9.21, PBS job 97288.asax-pbs1, revision 1fb5c20aebfdb95ba0bf6b7c2377c34d2282de79. This tiny exact computation does not need a GPU.

Public package execution needs Docker and the exact external artifacts. The historical acquisition and probe scripts contain the original Windows cache path, which must be relocated deliberately for another machine. They are original run receipts, not a one-command portable installer. Never alter a sealed script and present its execution as the original run. For a new environment, copy/version the runner, update paths, retain its hash and write to a new output directory.

1. Inspect top-level URLs/hashes in `protocol/public-evidence-v0.5-artifacts.json`, source records in the provenance audit, and the OSV archive identity in the selection manifest.
2. Inspect complete wheel locks: `protocol/langroid-v2-lock.json`, `protocol/pretalx-lock.json`, and `protocol/scrapy-compatible-lock.json`. Source-build receipts record the original commands and output hashes. A current resolver is not guaranteed to recreate those environments. Source-built wheel archives may differ even when their member bytes agree.
3. Obtain required public wheels and tokenizer data, checking all hashes before mounting them. Langroid's tokenizer URL/hash is in `protocol/langroid-tokenizer.json`. Certifi uses the original two pinned wheel bundles. No credentials are needed for these public files.
4. Read the per-case addenda and runner resource controls. Keep package hooks inside disposable build containers; keep behavior containers offline. Do not substitute a real target or host system directory for the synthetic fixture.
5. Run into a new directory and retain failed runs. The historical successful runners are `run_langroid_final.py`, `run_pretalx_probe.py`, and `run_public_behavior_compatible.py`; certifi is in the original `run_public_behavior.py` series. That original runner also includes the known failed Scrapy setup, so do not mistake it for a clean final all-case launcher.

The public archive, full papers, third-party wheels and tokenizer file are not redistributed in Git. Published identities and acquisition references support checking and reacquisition but cannot guarantee future availability. Do not replace a missing artifact without labeling a new environment and experiment.

The final Git release restores locally sealed raw bytes for files whose earlier Git blobs normalized line endings before preservation attributes were applied. Every such difference was checked to contain identical text after newline normalization. The affected-file ledger is `protocol/release-byte-preservation.json`. Use the final release for byte-hash verification; this correction changes neither observations nor algorithms.

## Manuscript

`paper/main.tex` is a standalone ACM-class manuscript with embedded bibliography, tables and TikZ diagram. The Overleaf ZIP needs no external images, dataset or bibliography file. Upload the ZIP, select main.tex, and compile with XeLaTeX or a compatible ACM-supported compiler. `nonacm` prevents invented acceptance/DOI/copyright metadata. Select a journal-specific production format only after choosing a venue.

The native Codex compiler failed before processing source with a runtime-directory error. A separate disposable-container Tectonic build succeeded, and its receipt is in `paper/build/receipt.json`. The final build runs offline against a previously populated official Tectonic bundle cache; it does not repair or replace the native editor. No unrelated manuscript was modified. The portable compiler archive was SHA-256-verified against its GitHub release digest. `src/build_manuscript.py --build-dir PATH` records a new build using that pre-acquired compiler and cache. It does not acquire them automatically. Overleaf import is the simpler portable manuscript route.

## Evidence boundaries

The public sample is deterministic, not representative. Successful probes are function-level or bundle-loading observations. WordOps is unsupported under the specified fixture; InvokeAI is excluded under the stable-fixed-release rule. No behavioral labels are assigned to either. The 24 failed probe-container runs and all preparation failures remain available. No paper acceptance, external preregistration, independent research-team replication, or operational remediation improvement is claimed.
