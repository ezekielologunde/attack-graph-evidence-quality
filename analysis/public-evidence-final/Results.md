# Final public-evidence feasibility results

The fixed first-six assessment is complete within its scoped fixture rules. Four narrow behavioral distinctions are confirmed, one case is excluded, and one fixture is unsupported. No case was replaced. Run `python src/verify_public_behavior.py` and `python src/analyze_public_final.py` to check saved observations.

| Rank | Package | Versions | Final disposition |
|---|---|---|---|
| 1 | InvokeAI | Only explicit fixed event 5.3.0rc1 | Excluded by stable-fixed-release rule |
| 2 | Langroid | 0.53.14 / 0.53.15 | Confirmed actual compute_from_docs expression-acceptance distinction, six final runs |
| 3 | pretalx | 2.3.1 / 2.3.2 | Confirmed actual dump_content export-path containment distinction, six runs |
| 4 | Scrapy | 2.11.1 / 2.11.2 | Confirmed both actual redirect middleware distinctions, six final runs |
| 5 | WordOps | 3.20.0 / 3.21.0 | Dependencies built; actual system-provisioning path unsupported by the frozen fixture |
| 6 | certifi | 2024.6.2 / 2024.7.4 | Confirmed specified certificate-store membership distinction, three paired runs |

## Controls and meaning

Langroid returns 2 for the benign DataFrame count in both versions, returns 2 for harmless len(df) only in the old version, and returns the expected sanitizer error in the fixed version. A malformed-expression control produces errors in both. The real method is invoked without constructing a vector store or embedding service. This is not a complete agent or arbitrary-code exploit test.

pretalx writes ordinary fixture bytes inside the export directory in both versions. A traversal input writes outside that export directory but inside its disposable parent fixture in 2.3.1; 2.3.2 raises CommandError and creates no such file. The getter returns synthetic bytes. No real event, external target, populated database or production export is involved. The separate media/static read path is not tested.

Scrapy and certifi controls and details are retained in the earlier behavior report. Across all executable cases, every predefined observation and control passes in three repetitions. There are 21 successful final container runs; repetitions are not independent vulnerabilities.

## Preserved failures and amendments

The original Scrapy noexec setup failed six times, its incompatible w3lib environment failed six times, the uncached Langroid import failed six times, and the initial Langroid Document fixture failed six times. All 24 failures remain available. Separately, wheel-only dependency resolution and Python 3.11 pretalx source builds failed; these are preparation attempts, not additional behavioral negatives. Versioned amendments and locks preceded corrected runs.

pretalx printed a startup banner before the JSON result. The runner recorded a parse_error despite exit zero. The final analyzer parses the unique complete JSON observation line from each original stdout, verifies it, and leaves the original flags unchanged. This is a reporting correction, not rerun or outcome replacement.

Langroid's independently built halo and wget ZIP artifacts had identical member bytes but different archive hashes. The final pair uses identical shared artifacts. pretalx also uses identical shared artifacts. Scrapy's fixed release adds defusedxml, an explicitly retained environment difference.

## Runtime and feasibility limits

Exact min/median/max probe times, median container elapsed time and maximum process RSS are in verified-results.json. Imports are inside probe timers. These are descriptive environment measurements; concurrent work was not controlled for performance comparison. They do not measure operational remediation or patch costs.

WordOps's real affected pre_pref function includes repository provisioning and hard-coded /etc writes. The frozen specification forbids provisioning and does not accept an extracted or mocked file-call fragment as evidence of a race. This is an unsupported fixture under the study scope, not proof of infeasibility under all environments, a reproduced vulnerability, or exhaustion of the two-hour engineering cap.

## Expansion decision

Proceed with the bounded methods and feasibility manuscript. Do not claim empirical remediation superiority or invent a mapping from these packages to graph priors, losses or costs. Broader system testing and calibration require a new protocol. Earlier reports are chronological records; this final disposition supersedes their pending statuses without rewriting them.
