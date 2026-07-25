<!-- AGENTTEAMS:BEGIN content v=1 -->
# Skill Generation Reference — LearnPythonStatsEcon

The capability-gap protocol: what to do when a request needs a resource this team cannot
already reliably access. Operative step: Workflow 0's "Capability gap check" in the
orchestrator.

## Trigger

**Attempted, not suspected.** This protocol applies after actually trying existing
capability — this team's declared tools/extensions, plus the discovery and installation
methodology in `references/cli-tool-discovery.reference.md` — and confirming it does not
reliably satisfy the request. Concluding "I don't have a tool for this" without first working
the gap is exactly the failure mode this reference exists to close.

## If direct access succeeds

Just do it. This protocol only applies once existing capability has genuinely been tried and
found insufficient — it is not a mandatory detour for requests that are already fulfillable.

## If it doesn't: two-part response, not a bare refusal

1. **Best-effort access now.** If any partial path exists — a manual workaround, a
   lower-fidelity substitute, a nearby tool that gets close — use it and say plainly what it
   does and doesn't cover.
2. **A plan to build durable infrastructure for reliable future access.** Examples: wiring in
   a needed extension, installing a missing CLI tool (per
   `references/cli-tool-discovery.reference.md`, subject to its Security Rule S-4 clearance
   requirement), or adding a small script. Surface the option to build the capability — don't
   stop at reporting that it's unavailable.

## Worked example: a page `fetch` can't render

A concrete instance of the two-part response above, for a request that keeps recurring across
frameworks: a task needs content from a page that only appears after JavaScript runs (a
client-rendered app, a page behind a "loading..." skeleton, content injected by a framework like
React/Vue after the initial HTML). A plain HTTP fetch — this team's own static text-fetch tool, or
a bare `curl`/`wget` from a shell extension — returns the pre-render shell, not the real content.
That is a genuine capability gap, not a reason to give up: work it in tiers, cheapest first, and
verify each tier before assuming it or the next one is needed.

1. **Tier 1 — static fetch/search, if this project already has it.** Check for an existing
   text-search-and-fetch capability the same way `references/cli-tool-discovery.reference.md`
   teaches for any CLI tool — don't assume presence or absence. If it works for this page, stop
   here; it's the cheapest tier and most pages don't need more.
2. **Tier 2 — real browser rendering, only once Tier 1 is confirmed insufficient.** The durable-
   infrastructure answer here is **the pattern**, not one specific tool: a small, dependency-gated,
   project-owned CLI wrapper around a browser-automation library (e.g. Playwright), invoked via
   shell, that (a) renders the page with JavaScript enabled, (b) extracts text from the rendered
   result, and (c) re-applies this project's own URL-safety check to **every** request the live
   page attempts — not just the one URL a caller typed in, since a real browser follows redirects
   and runs page JavaScript that can issue its own requests to other hosts. A single check of the
   original URL alone does not cover that; if you build this for a project that already has an
   HTTP-fetch safety guard, reuse it as the per-request check rather than writing a second, looser
   one.
   - **If this project is Python-based** (or the operator is willing to add a Python runtime for
     this), `agentteams` ships a ready-made instance of exactly this pattern:
     `agentteams.research.browser` (`python -m agentteams.research browser "<url>" [--headed]`),
     gated behind the separate `agentteams[browser]` optional install
     (`pip install agentteams[browser]` **and** a one-time `playwright install chromium`) so a
     project that only wants lightweight text search never pays for it. `--headed` shows the
     browser window — useful only when a human operator is watching the same machine locally
     (debugging, a manual login/2FA step); it changes nothing about what the calling agent itself
     receives back, which is the same extracted text either way.
   - **If this project is not Python-based**, the pattern still applies: the equivalent in this
     project's own ecosystem (e.g. a Node script around Playwright's own JS bindings) is the
     durable-infrastructure answer, built and gated the same way — don't reach for a Python tool a
     non-Python project has no reason to depend on.
3. **Neither tier reaches it, or the browser tier isn't installed yet.** That absence is itself the
   capability gap this protocol exists for — proceed to the "Output and ownership" plan mechanism
   below, don't just report the page as unreachable.

## Security audit gate — before use or persistence, not after

Before acting on either part of the two-part response above, check the pathway (the specific
command, install step, URL/API fetch pattern, or script the best-effort access or the
durable-infrastructure plan depends on) against `security.template.md`'s Rule S-9 (Pathway
Safety Verification) risk criteria. This applies whether or not you intend to persist
anything — a pathway can need this gate for a single, one-off use.

- **Matches none of Rule S-9's 5 criteria** (the common case — an official-source install, a
  read-only lookup, a routine fetch of public data): proceed. This gate does not apply and
  does not require `@security` involvement.
- **Matches one or more criteria**: request `@security` review under Rule S-9 before doing
  either of the following — do not do them first and check after:
  - Using the pathway to produce output for the user this turn.
  - Writing the pathway into `references/cli-tool-discovery.reference.md`, this file, or any
    other reference/skill a future session will read and act on unattended.
- **HALT** blocks both the one-time use and persistence — report the blocker, do not work
  around it.
- **CONDITIONAL PASS** permits the one-time use under the stated conditions but **blocks
  persistence** until `conditions_verified` is set (same rule this project already applies to
  every other `CONDITIONAL PASS`, per the orchestrator's Pre-Execution Security Check).
- Only a clean **PASS**, or a `CONDITIONAL PASS` with `conditions_verified` confirmed, permits
  writing the pathway into a reference/skill file for future reuse.
- Log the verdict to `references/security-decisions.log.csv` — the same log every other
  `@security` verdict in this project already uses. Do not invent a separate record of this
  decision.

This is a narrower, higher-stakes cousin of `retrospective-remediation.reference.md`'s
Content-Safety Rule: that rule keeps an ordinary remediation-log text append free of any
security gate. This one is deliberately not that permissive, because what's at stake here is
content a future agent will **execute**, not a sentence describing a past event.

## Output and ownership — reuse this project's own plan mechanism

Part 2 is itself multi-step work. It does not get a free-floating suggestion; it follows this
team's own mandatory-plan rule exactly like any other multi-step request:

- A summary at `tmp/by-week/YYYY-Www/<plan-slug>.plan.md` and a step CSV at
  `tmp/by-week/YYYY-Www/<plan-slug>.steps.csv`, before the first infrastructure-building step
  executes.
- The agent that hit the gap opens that plan.
- If closing the gap means changing this team's own generated agent infrastructure (a
  template, a framework adapter, a routing rule) rather than a one-off local install, route
  through the orchestrator to the relevant specialist instead of acting solo — the same
  routing discipline that applies to any other domain-specific change.
- The plan gets the same audit chain as any other plan: `@adversarial` and `@conflict-auditor`
  before execution, and after each completed step.

## Why this exists

A team that only ever reports "I can't do that" for a genuinely reachable or buildable
capability under-serves every future request of the same shape. This reference exists so that
a confirmed capability gap becomes a scoped, auditable plan — not a dead end, and not an
unaudited ad hoc fix either.
<!-- AGENTTEAMS:END content -->
