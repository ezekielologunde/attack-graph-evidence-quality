# Frozen finite validation v0.4

ASA-X PBS job `97288.asax-pbs1` executed commit `1fb5c20aebfdb95ba0bf6b7c2377c34d2282de79` on 2026-10-07. All sealed input hashes matched. All 96 cases completed, yielding 960 policy rows and no reported failures. Raw files were downloaded through Open OnDemand and verified against the compute-generated SHA-256 manifest.

Primary endpoint: lineage_age_voi expected loss minus lineage_age_immediate expected loss. Negative values favor verification. Counts use the prespecified tolerance of 1e-9.

| Graph | Cases | Lower loss | Tie | Higher loss | Minimum | Median | Maximum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Diamond | 32 | 16 | 16 | 0 | -1.0 | -0.2125 | 0 |
| Shared bridge | 32 | 0 | 32 | 0 | 0 | 0 | 0 |
| Bypass cycle | 32 | 11 | 21 | 0 | -0.65 | 0 | 4.44e-16 |

Verification lowered modeled loss in 27 cases and tied in 69. The shared-bridge zero-benefit cases are retained as specified. These are exact calculations on a deliberately specified synthetic grid, not independent empirical samples or evidence of population superiority. No p-values or population confidence intervals are reported. This result does not establish novelty, real-world calibration, or end-to-end remediation effectiveness.

The original frozen protocol retains its pre-execution wording to preserve its hash. This report records its subsequent execution. The next scientific step is examination of per-case decisions and secondary endpoints, followed by a separately specified empirical or expanded validation protocol.

The run used Python 3.9.21, one CPU and a 1 GB memory request in the express queue. The runner logs UTC times, source commit, sealed inputs, decisions, spends, oracle regret and dropped conflicting groups. Results remain outside the checkout on ASA-X at `/home/lawexo001/attack-graph-runs/validation-97288.asax-pbs1`.
