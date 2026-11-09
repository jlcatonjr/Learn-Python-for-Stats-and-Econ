# Coordination Request (2026-W46): operator home path in tracked files (Learn-Python-for-Stats-and-Econ)

**From:** infrastructure-management orchestrator · **Date:** 2026-11-09 · **Protocol:** 3 (orchestrator-to-orchestrator)
**Target:** Learn-Python-for-Stats-and-Econ (jlcatonjr/Learn-Python-for-Stats-and-Econ, default branch `master`, visibility **PUBLIC**)
**Channel:** mediated. The operator delivers this document as a PR. It carries no directive authority, and Learn-Python-for-Stats-and-Econ's team
decides what to do.
**Requested by:** the operator, live in session infrastructuremanagement-99 on 2026-11-09 ("Send requests").
**Origin:** finding S-8 in the 2026-11-08 manager-roster rollout (SEC-IM-ROSTER37 delta 10). In this document the
path is written as `/Users/<user>/…`.

## Finding

Files tracked on `master` contain the operator's absolute home path (`/Users/<user>/githubrepositories/…`). It shows
the local username and directory layout, in a public repository. Files counted on 2026-11-09 against the local checkout, with `git grep -lI` for text files and `git grep -l` for binary ones:

- `brief.json`: `existing_project_path`
- `.github/agents/.agentteams-backups/<timestamp>/_manifest.json`: 8 files (`description_path`, `output_root`,
  `source_path`)
- `In Class Projects/datlib/__pycache__/*.pyc`: 4 files

## What is asked

1. Remove the absolute path from the files above or make it relative: drop `existing_project_path` or set it to `.`,
   and read configuration paths from an environment variable or a path relative to the repository.
2. Untrack agentteams backup and fleet-report folders (`.agentteams-backups/`, `.agentteams-fleet/`) where they are
   tracked, and add them to `.gitignore`. They are generated per run and record absolute paths by design.
3. Untrack committed `__pycache__/*.pyc` files and add them to `.gitignore`, where they appear.
4. Use your own team's plan, review and clearance for any removal.

**Not asked:** no history rewrite or force-push. The path is low sensitivity, and rewriting history is destructive
(C-5). If your team wants one, it's a separate decision with its own clearance.

## Note on the tool

Some of these files are written by agentteams (`_manifest.json`, `build-log.json`, `_build-description.json`). A
hand edit to a generated file can come back on the next `--update`. infrastructureManagement records the tool-side
part separately; this request covers only what your repository tracks.

## Reply

Reply on the PR, or tell the operator. infrastructureManagement tracks this as OI-2026-11-09-03
(`docs/open-items-2026-11-09.md`).
