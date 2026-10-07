# Research portfolio and execution order

Completion update, 7 October 2026: the attack-graph study now has a complete 12-page ACM-class manuscript with two diagrams and six tables, verified synthetic and public results, a compiled PDF, and an Overleaf package. See `../paper/README.md`. The scoped first-six audit closes with four narrow checks, one exclusion and one unsupported fixture. The earlier checklist below is retained as planning history. Author review and actual journal submission remain distinct; the next proposed project is the intrusion-detection novelty/dataset audit.

Decision recorded 7 October 2026: finish the current attack-graph evidence-quality project before starting the next project. This document is a plan, not a claim of novelty or completed experiments.

## Sequence

1. **Active: attack-graph evidence quality.** Complete the bounded study, evidence audit, reproducibility package, and submission-ready manuscript using the completion checklist below.
2. **Next proposed lead: reliable intrusion detection under missing telemetry and domain shift.** Begin with a novelty and dataset feasibility audit. Do not start large training before this gate passes.
3. **Queued: adaptive cyber defense under delayed and unreliable observations.** Prioritize evidence-gathering versus action costs, beyond existing topology-transfer work.
4. **Queued: AI-agent security under changing tool environments.** Evaluate defensive security and legitimate task usefulness in isolated benchmark environments.
5. **Queued: vulnerability detection with incomplete code context.** Investigate calibrated context requests and abstention on unseen projects.
6. **Retained education selections:** reliable student predictions under population/temporal shifts and robust models with incomplete learning records. Share infrastructure where useful but justify separate papers independently.

The user selected all AI cybersecurity directions for consideration, not simultaneous implementation. The next proposed lead reflects the current recommendation; a failed novelty or data gate can change that order with a documented reason.

## Current-project completion checklist

### Evidence already available

- Exact development cases: original pilot, shared-path v0.2, integrated v0.3.
- Frozen v0.4 validation: 96 cases, 960 policy rows, zero execution failures on ASA-X job 97288.asax-pbs1. Primary difference favors verification in 27 cases and ties in 69, tolerance 1e-9.
- One public advisory-lineage audit, two package versions, a narrow 16-case offline API behavior check, and two actual scanner comparisons.
- These demonstrate bounded feasibility. They do not establish empirical generalization, calibrated operational probabilities, or novelty.

### Required remaining work, in order

1. **Analyze existing results without new tuning.** Verify all input/output manifests and reproduce the primary summary from raw rows. Tabulate decisions, costs, oracle regret, conflict handling, and outcomes by graph/prior/evidence/cost. Explain zero-benefit and harmful-policy cases. Label newly selected subgroup analyses exploratory.
2. **Resolve the contribution.** Refresh the closest-paper comparison and record what is reused, what is extended, and what remains unsupported. Standard value of information, graph dependence, and source deduplication alone are not novelty claims. Do not describe structural reachability as an equivalent implementation of a finite-horizon attacker model.
3. **Freeze an empirical feasibility protocol.** Specify publicly retrievable advisory/package cases, inclusion criteria, independent behavioral evidence where feasible, negative controls, provenance relationships, and measurable decision costs. Choose sample scope before outcomes. If broader evidence is infeasible, retain a bounded methods/case-study claim rather than promise generalization.
4. **Execute only the frozen extension.** Preserve failed runs, exclusions, source dates, package identities, scanner versions, hashes, and acquisition licenses. Use local isolated tests for service interactions and HPC only for substantial portable batch work.
5. **Audit validity.** Check leakage, duplicated upstream evidence, dependence among cases, sensitivity to assumed costs/probabilities, and whether conclusions survive realistic measurement uncertainty. Separate modeled loss from observed remediation outcomes.
6. **Package reproducibility.** Pin environments and sources; add one-command analysis, data dictionary, acquisition instructions, experiment manifest, and compute/resource accounting. Verify from a clean environment. Publish redistributable originals only.
7. **Prepare manuscript and Overleaf package.** Include complete methods, related work, limitations, results, diagrams, tables, bibliography, and data/code availability. Select an ACM journal based on the actual contribution and requirements. Compile and inspect the final package. This project uses its own manuscript; do not overwrite the digital-twin paper.
8. **Final consistency audit.** Every number must trace to raw outputs; every novelty statement must survive the literature comparison. Record unresolved issues explicitly. A negative or limited finding is acceptable; manufactured novelty is not.

**Completion gate:** steps 1-8 have concrete artifacts, all material discrepancies are resolved or disclosed, and a reproducible submission-ready package exists. Actual journal submission/acceptance is tracked separately and must never be implied by GitHub publication. Confirm destination and remaining author metadata for submission. Journal review need not block starting the next project.

## Candidate research designs and compute placement

| Project | Candidate question | Data or environment | Essential comparisons | Compute placement |
|---|---|---|---|---|
| IDS reliability | Can selective prediction maintain useful detection under joint domain and telemetry changes within an analyst budget? | Compatible NetFlow datasets; verify versions, schema, labels, license and split units first | Conventional tree models, neural baselines, calibrated abstention; held-out domains and missingness; no test-set threshold tuning | Local schema/debug work; HPC training and repeated evaluation |
| Adaptive defense | When should a defender acquire evidence rather than act under delayed or unreliable observations? | CybORG/CAGE Challenge 4 with pinned simulator and documented modifications | Heuristic, PPO and relevant graph-based agents; unseen scenarios; service disruption and sensing costs | HPC parallel CPU rollouts and GPU training; local simulator checks |
| Agent security | Do defenses preserve task usefulness as tool schemas and workflows shift? | AgentDojo and relevant extensions, synthetic accounts/tools only | Undefended and published defenses; held-out tasks; security, benign completion, latency and compute | HPC open-weight inference; local benchmark validation |
| Code vulnerability reliability | Can a model request useful context or abstain on unfamiliar projects? | PrimeVul and independently audited compatible sources | Static-analysis and code-model baselines; project/time separation; paired vulnerable/fixed cases where appropriate | HPC adaptation and inference; local data audit |
| Learned graph verification | Can learned policies approach exact decision quality on larger graphs? | Existing model and openly specified graph generators | Exact methods where tractable, heuristics; regret, runtime, distribution shifts | Future extension only; HPC for genuinely large generation/training |
| Education transfer | When should prediction abstain after population or temporal change? | EdNet and suitable ASSISTments versions after compatibility audit | Conventional and neural knowledge-tracing baselines; calibration and coverage | Local pilot; HPC repeated training |
| Education missing records | How do missing attempts, hints or timestamps change mastery predictions? | Timestamped educational logs with verified observables | Random and structured missingness; multiple models; predictive rather than causal claims | Local preprocessing; HPC experimental grid |

Existing digital-twin Docker experiments remain local unless converted to a supported cluster workflow. ZKP benchmarks are conditional on demonstrated computational need and software compatibility. Autonomous pentesting work is limited to authorized isolated testbeds; HPC work should be offline training/simulation within facility rules. Adaptive deception is considered with the adaptive-defense track, with a separately specified question if advanced.

## ASA-X resource plan

Documentation inspected 7 October 2026 lists A100/H100 nodes, including 80 GB and 94 GB GPU configurations. GPU queue documentation permits requests for up to two GPUs and lists up to 360 hours, 24 CPU cores and 120 GB host RAM. Large CPU queue lists up to 128 cores and 120 GB. Host RAM is not GPU memory. These figures describe documented facilities, not exclusive access or a verified allocation for this account.

CPU execution and browser-terminal command entry were demonstrated earlier. A fresh GPU allocation, installed ML stack, current concurrency, storage quota and account-specific entitlement remain unverified. The previous terminal was not attached at the last check. Larger restricted queues are not assumed available.

Before GPU research:

- Reconnect the authenticated browser shell; user handles password/Duo.
- Inspect current qlimits, GPU queue constraints, quota and supported GPU submission documentation.
- Submit a minimal scheduled GPU check, recording model, memory, driver/runtime and framework compatibility. Do not run training on login nodes.
- Pilot one representative workload. Record peak host/GPU memory, CPU/GPU utilization, runtime, storage and output volume.
- Estimate the full experiment budget from measured runs; request a reasonable margin and obey concurrency limits. Checkpoint jobs and retain restart metadata.
- Scale to two GPUs only if the implementation supports it and measured throughput justifies it. More requested resources can increase waiting time.
- Treat scratch as temporary: documentation requires removal of results within seven days after a job and warns of deletion during maintenance. Use it only for an appropriate documented workflow.

No large training jobs, model downloads or new project launches are authorized by this planning document alone. The current user instruction is sequencing and planning; implementation resumes on the current attack-graph project first.

## Repository and publication conventions

Each active project has a repository with protocol, source, tests, analysis, data provenance, HPC scripts, and manuscript directories. Keep planned versus executed status explicit. Commit versioned protocols before evaluation. Store large/restricted data and checkpoints outside Git, with acquisition scripts, licenses and hashes in Git. Do not publish credentials or private participant data.

Author: Ezekiel Ologunde. Affiliation: Independent Researcher. Author email: ologunde@bu.edu. No corresponding-author designation, as requested. Original work remains unlicensed by choice; third-party terms remain in force. ACM is the intended publication family, not a claimed publisher relationship, accepted venue or assigned DOI.

## Literature leads and verified documentation

This is an initial screening list, not a systematic review or novelty clearance. Some leads are preprints. Recheck versions and read full texts at project initiation.

- ASA-X hardware: https://hpcdocs.asc.edu/content/asa-x-hardware
- ASA-X queue policies: https://hpcdocs.asc.edu/content/pbs-queue-system
- Cross-Domain Generalization Strategies for IoT Cyberattack Detection Using Flow-Based Features (2026): https://doi.org/10.1016/j.iot.2026.102044
- TERLA, topology generalization: https://arxiv.org/abs/2511.09114
- CybORG CAGE Challenge 4: https://github.com/cage-challenge/cage-challenge-4
- AgentDojo: https://agentdojo.spylab.ai/
- AutoDojo: https://arxiv.org/abs/2606.15057
- PrimeVul: https://github.com/DLVulDet/PrimeVul
- Context-aware vulnerability detection: https://arxiv.org/abs/2602.06751
- EdNet: https://arxiv.org/abs/1912.03072
- Knowledge tracing over time: https://educationaldatamining.org/EDM2023/proceedings/2023.EDM-short-papers.28/2023.EDM-short-papers.28.pdf

Immediate next action: complete the existing attack-graph v0.4 secondary analysis and evidence audit. Do not start the next model-training project yet.
