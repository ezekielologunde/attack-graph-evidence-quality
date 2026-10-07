# Full text comparison and study scope

6 October 2026. This supplement supersedes the two PDF access blockers in the v0.2 comparison. Both source PDFs were retrieved directly with PowerShell after browser retrieval failed. Methods, examples and discussion passages were extracted with pypdf. Source hashes and bibliographic records are in `literature-sources-v0.3.json`. PDFs and extracted full text remain outside this repository. This is targeted methods review, not independent reproduction or exhaustive novelty clearance.

## Nguyen and colleagues

[An Approach to Incorporating Uncertainty in Network Security Analysis](https://publish.illinois.edu/science-of-security-lablet/files/2014/05/An-Approach-to-Incorporating-Uncertainty-in-Network-Security-Analysis-1.pdf), HoTSoS 2017, DOI 10.1145/3055305.3055308.

Sections 3 and 4 represent edge existence through Boolean expressions of shared independent indicators and analyze monotone uncertainty bounds. This overlaps directly with shared gates and possible-world reachability. Section 4, Remark 2, explicitly motivates identifying where further information would most reduce uncertainty, referring to sensitivity analysis. Section 5.2 also asks how hardening changes reachability. Sections 5 and 6 supply Stuxnet and enterprise illustrations; section 6.3 defers numerical analysis to follow-up work.

**Bounded distinction:** the inspected methods do not specify our copied-report observation likelihood, erroneous source labels, noisy query followed by patch choice, or a joint query/patch budget experiment. This is a difference from this paper, not proof of an unfilled field-wide gap. Its uncertainty-reduction discussion means we must not present information gathering for attack-graph analysis as new.

## CAPG v2

[CAPG-v2](https://www.scitepress.org/Papers/2026/150641/150641.pdf), SECRYPT 2026, pp. 1089-1096, DOI 10.5220/0015064100004103.

Sections 3 and 4 distinguish conditional exploit-success probability from attacker action selection. Equation 1 is an independent-prior path product; section 4.2 instead simulates finite-horizon attempts under an attacker policy, with failed attempts leaving the state unchanged. Patching disables all transitions bearing a CVE. Section 4.3 evaluates patch budgets. The schema includes evidence level, so claiming it ignores evidence would be false.

Sections 5-7 report a demo with 18 assets and 25 vulnerability instances, varied topology, seeds and attacker policies. The authors identify unvalidated input probabilities/losses, demo scale and simplified attacker policies as limitations, proposing sensitivity, feasibility evidence and temporal extensions.

**Bounded distinction:** the specified evaluator does not include our paid noisy verification action or erroneous copied-report lineage. These omissions in the described experiment support a possible extension, not priority. No artifact link was found in extracted PDF hyperlinks; a GitHub repository-name search did not identify its evaluator. Artifact availability remains unresolved, not disproven.

## The outcome mismatch that must be fixed

Our current endpoint is the expected weighted number of reachable targets across latent network states. It measures structural exposure under the modeled distribution. CAPG's rollout endpoint additionally depends on action selection, attempt success, retries and horizon. Sharing the term expected loss does not make the two numerical quantities interchangeable.

For our endpoint, removing enabled edges cannot increase reachability in any fixed state. Consequently, under the same state distribution and nonnegative target weights, adding patches cannot increase expected structural loss. This is a mathematical model property, not an empirical claim about attackers or production safety.

For contrast, consider an illustrative one-step attacker with two available successful actions, one reaching a target with loss 10 and one reaching a harmless dead end. Uniform selection gives expected attacker loss 5. Removing the harmless action and renormalizing selection gives loss 10. Structural target reachability remains 1 before and after. This hand-derived example explains why an attacker-policy metric can change differently; it is not a reproduction or criticism of CAPG's results.

## Research decision

Proceed with a **structural exposure benchmark under imperfect evidence**. Keep the existing small pilots as development examples. Do not call the model a calibrated attacker simulator, a reproduction of CAPG, or a new uncertainty formalism. Public topology data can ground graph structure but cannot by itself calibrate observation accuracy or correlated reporting errors.

Working question: under equal total cost, when do mistaken assumptions about observation lineage change whether verification is preferable to immediate patching, and how sensitive is that decision to shared graph dependencies?

The most defensible candidate contribution is a benchmark and failure-boundary analysis. Its novelty remains conditional on the wider active-diagnosis, security-game and source-dependence literature. This pass resolves access to two close papers, not the entire novelty question.

## Next implementation contract

1. Integrate v0.1 source groups and stale-observation likelihoods with v0.2 graph reachability. Keep the evaluator's true grouping inaccessible to policies. Label correctly specified beliefs as privileged-model comparators.
2. Separate two kinds of dependence: shared latent graph facts and copied measurement events. Do not represent copied observations as independently sampled evidence or infer measurement correlation merely from shared paths.
3. Include immediate patching, ordinary deduplication plus VOI, naive VOI, uncertainty-based queries and a diagnostic oracle at equal total budget. Keep expensive-query and universal-cut controls.
4. Define a mismatch grid before evaluation: reported-source splitting/merging, age-model errors, query accuracy and budget opportunity cost. Conflicting reports assigned to one group require an explicit policy, not silent first-row selection.
5. Freeze training/development and held-out topology families before collecting held-out results. Select parameters without consulting the held-out evaluator. Report paired loss differences within each scenario and dependence-aware aggregation across topology families.
6. Treat finite-horizon attacker dynamics as a separately specified extension if needed later. Do not rename current structural loss as observed attack frequency.

No new experiments were run for this literature supplement. No final novelty, field effectiveness or publication claim is made.
