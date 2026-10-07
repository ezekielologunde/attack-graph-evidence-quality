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

Share the preflight output with this chat. It checks limits, quota, Python, Git and express-queue resource fields. It does not dump environment variables or read SSH keys. Python 3.11 or later and Git are required; the model uses only Python's standard library. Do not install Docker or assume Docker is allowed on compute nodes.

## First queued job

The requested smoke-test envelope is one CPU, 4 GB RAM and 15 minutes, subject to current queue rules. `smoke.pbs` deliberately contains no queue or resource directives until ASA-X's resource syntax and Python module are confirmed. Do not submit it using unknown defaults. Submit from the repository directory with the confirmed queue/resources. Avoid qsub -V, which exports the whole login environment.

Before submission record `git rev-parse HEAD` and keep that checkout unchanged until the job completes. The runner rejects changed tracked files and mismatched frozen hashes. It writes outside the checkout to `$HOME/attack-graph-runs/smoke-PBS_JOBID`, refuses to overwrite that run, and records the actual commit, job ID, Python version, test logs and SHA256 manifest. No random seeds are needed for these deterministic unit checks.

## Return and GitHub workflow

Download only the run directory and scheduler log after the job finishes. Verify its manifest locally, inspect failures, and then commit suitable result summaries and provenance through the existing local GitHub workflow. Do not put GitHub credentials on the cluster just to upload results. Large datasets stay in approved cluster storage; publish acquisition instructions and hashes rather than blindly committing them.

This preparation does not establish SSH access from this chat, successful PBS submission, Python-module availability or cluster execution. ASA's public documentation page states that detailed HPC documentation requires account login: https://asc.edu/service/hpc-documentation . Resource syntax remains pending preflight and site documentation. The earlier sealed validation protocol is unchanged; a separate versioned execution wrapper must be reviewed before that study is run.
