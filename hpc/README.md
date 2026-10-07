# ASA-X CPU handoff

Scope: continue attack-graph evidence-quality research. No intrusion-detection dataset project, GPU training or new journal claim is introduced. The first cluster run is a portability check of the existing 26 tests and frozen input hashes, not execution of the 96-case prospective study.

## Login and preflight

The user's setup notes identify `lawexo001@asax.asc.edu` and PBS. These are historical connection details, not a verified current session. Password and Duo input remain with the account owner. No credentials or GitHub token are required to clone the public repository.

After SSH login, use a new project directory:

```sh
git clone https://github.com/ezekielologunde/attack-graph-evidence-quality.git
cd attack-graph-evidence-quality
bash hpc/preflight.sh
```

Share the preflight output with this chat. It checks limits, quota, Python, Git and express-queue resource fields. It does not dump environment variables or read SSH keys. Python 3.9 or later and Git are required for this smoke test; the model uses only Python's standard library. Do not install Docker or assume Docker is allowed on compute nodes.

## First queued job

Live preflight on 7 October 2026 confirmed express limits of 1-4 CPUs, at most 16 GB, and wall time between one and four hours. The system interpreter is /usr/bin/python3, version 3.9.21. The PBS file now requests one CPU, 4 GB and one hour. One hour is a queue minimum, not an expected runtime.

The unchanged 26-test suite passed locally under Python 3.9 in an isolated Linux container (image digest sha256:2d97f6910b16bd338d3060f261f53f144965f755599aab1acda1e13cf1731b1b). This supports lowering the smoke wrapper's minimum version; frozen research code and input hashes were not changed. Actual ASA-X execution remains to be checked.

From the cloned repository on ASA-X:

```sh
git pull --ff-only && qsub hpc/smoke.pbs
```

Save the returned job ID. Do not resubmit merely because a job queues. Use `qstat JOB_ID`; after completion inspect `~/attack-graph-runs/smoke-JOB_ID/run.json` and `tests.stderr.txt`, plus the PBS log in the submission directory. A qstat entry disappearing is not proof of success. Avoid qsub -V, which exports the entire login environment.

Before submission record `git rev-parse HEAD` and keep that checkout unchanged until the job completes. The runner rejects changed tracked files and mismatched frozen hashes. It writes outside the checkout to `$HOME/attack-graph-runs/smoke-PBS_JOBID`, refuses to overwrite that run, and records the actual commit, job ID, Python version, test logs and SHA256 manifest. No random seeds are needed for these deterministic unit checks.

## Return and GitHub workflow

Download only the run directory and scheduler log after the job finishes. Verify its manifest locally, inspect failures, and then commit suitable result summaries and provenance through the existing local GitHub workflow. Do not put GitHub credentials on the cluster just to upload results. Large datasets stay in approved cluster storage; publish acquisition instructions and hashes rather than blindly committing them.

The live terminal confirms SSH login and preflight, but this chat can only read that terminal. Successful PBS submission and compute-node execution remain unverified. ASA's public documentation page states that detailed HPC documentation requires account login: https://asc.edu/service/hpc-documentation . The request uses the PBS ncpus, mem and walltime resources shown by the live queue output; scheduler acceptance must still be checked. The earlier sealed validation protocol is unchanged; a separate versioned execution wrapper must be reviewed before that study is run.
