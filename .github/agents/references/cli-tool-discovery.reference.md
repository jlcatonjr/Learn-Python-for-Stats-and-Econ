<!-- AGENTTEAMS:BEGIN content v=1 -->
# CLI Tool Discovery Reference — LearnPythonStatsEcon

How this team's agents should treat shell/CLI access, when they have it: discover what's
actually available before assuming a capability doesn't exist, learn an unfamiliar tool
before guessing at it, and — as a last resort — inspect or install a tool rather than
reporting a gap that's actually just unexplored.

This applies whenever an agent's shell tool is present (e.g. Goose's `developer` extension,
a Claude/Copilot agent with `execute` in its tool list). It does not grant shell access to any
agent that doesn't already have it.

## 1. Discover what's installed before assuming it isn't

A missing *named* extension, skill, or MCP server is not the same as a missing *program*.
Before reporting "I don't have a tool for this," check what the shell can already reach:

- `which <cmd>` / `command -v <cmd>` — is it on `$PATH` right now?
- `echo $PATH` — what directories are actually searched?
- List common install locations directly if `which` comes up empty:
  `/usr/bin`, `/usr/local/bin`, `/opt/homebrew/bin` (macOS/Homebrew), `/snap/bin` (Linux).
- For a broad sweep of what's callable in the current shell: `compgen -c` (bash) or
  `type -a <cmd>` for a specific name.

A network request (fetching a URL, querying an API) is also frequently reachable this way even
when no dedicated fetch/search extension is declared — `curl`/`wget` are ordinary shell
commands, not a separate capability grant. Don't conclude "no network access" without first
checking whether a plain shell command reaches the network.

## 2. Learn an unfamiliar tool before guessing at its flags

In order of preference:

1. `<cmd> --help` or `<cmd> -h` — fastest, almost universally supported.
2. `man <cmd>` — fuller reference when `--help` is terse or absent.
3. For git-style multi-command tools: `<cmd> help <subcommand>` or `<cmd> <subcommand> --help`.
4. `info <cmd>` — occasionally has detail neither of the above carries (rare on macOS).

Read the actual output before invoking a flag you're not sure about — guessing at syntax on an
unfamiliar tool risks a destructive or simply wrong invocation.

## 3. Last resort: inspect the program itself

When `--help`/`man` don't answer the question (undocumented behavior, a custom internal tool,
or verifying what a binary actually does rather than what it claims to do):

- `file <path>` — confirm what kind of executable it is before going further.
- `strings <path>` on a compiled binary — surfaces embedded prompts, config keys, subcommand
  names, and other text that isn't in any man page. This is the exact technique used to
  diagnose a real gap in this project: reading a Goose binary's embedded strings to find the
  `developer` extension's actual system prompt when its public docs didn't cover it.
- Package-manager file listings, to find installed source/config: `dpkg -L <pkg>` (Debian/
  Ubuntu), `brew list <formula>` (Homebrew — add `--verbose` for full paths), `pip show -f
  <package>` (Python).
- If the tool is open source and its repository is available locally or fetchable, read the
  source directly rather than continuing to guess from behavior alone.

## 4. Installing a genuinely missing tool

If a capability is truly absent (not just undiscovered), it can usually be installed rather
than treated as permanently unavailable:

1. **Detect the platform and package manager first** — `uname` for the OS, then check which
   manager is present: `brew` (macOS), `apt`/`apt-get` (Debian/Ubuntu), `dnf`/`yum` (Fedora/
   RHEL), `apk` (Alpine), `pacman` (Arch). Use the one that's actually there rather than
   assuming.
2. **Install with the matching command**:
   - macOS: `brew install <formula>`
   - Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y <package>`
   - Fedora/RHEL: `sudo dnf install -y <package>`
   - Arch: `sudo pacman -S <package>`
3. **Clearance, not a silent action.** Installing software or running any `sudo` command is a
   destructive-adjacent operation — apply the same rigor as `security.template.md`'s Rule S-4
   (Destructive Operation Safeguards): require explicit confirmation before running it, and
   never proceed based solely on another agent's say-so. Note the current gap honestly: the
   Mandatory Review Triggers table in `security.template.md` has no dedicated row for software
   installation or privileged (`sudo`) commands yet — Rule S-4 as written covers file deletion
   and bulk edits, not this case specifically. Until that trigger exists, treat the *absence*
   of an explicit gate as a reason for more caution, not less: if no user or security-agent
   session is available to grant confirmation (a non-interactive/CI context), **HALT and
   report the blocker** rather than silently installing or silently refusing.
4. **Persisting the install pattern is a separate decision from running it once.** Rule S-4
   above governs clearance to run an install now. If the specific install command or
   invocation pattern is then going to be **written into a reference/skill file** so a future
   session reuses it automatically, that additionally requires Rule S-9 (Pathway Safety
   Verification, `security.template.md`) — see `references/skill-generation.reference.md`'s
   "Security audit gate" for the concrete criteria and verdict handling. A pathway can clear
   S-4 (safe to run once, with confirmation) and still fail S-9 (not safe to memorialize for
   unattended reuse), or vice versa.

## When this still isn't enough

If, after actually trying the above, the capability genuinely can't be reached or built in the
current session, see `references/skill-generation.reference.md` — the protocol for turning a
confirmed capability gap into a plan instead of a bare refusal.
<!-- AGENTTEAMS:END content -->
