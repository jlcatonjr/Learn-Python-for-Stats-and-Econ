<!-- AGENTTEAMS:BEGIN content v=1 -->
# External-Retrieval Quality Gate Reference — LearnPythonStatsEcon

The mandatory final check before presenting any summary that relies on externally-retrieved
information — web search results, fetched page content, or documentation looked up from a
third-party source. Operative for any agent whose procedure links here: the gate step in that
agent's own instructions is where this reference is invoked from.

## Scope

Applies to any final summary, finding, or filled-in value that includes externally-retrieved
information: a URL or citation, a quoted or paraphrased claim attributed to a source, fetched
page content, or a third-party documentation excerpt. Does not apply to purely internal work
(content derived only from this project's own files, prior agent output already audited by this
project's normal close-out process) — that already has its own audit path and doesn't need this
one duplicated on top.

## Trigger

**Before presenting the summary as done, not after.** This is the final step of the producing
agent's own procedure, not an optional follow-up a human clicks. A summary that skipped this gate
is not a completed deliverable — it is a draft.

## The gate

1. **Hand off the complete draft** — every claim and every link/citation it rests on — to
   `@adversarial`. Ask it to challenge each claim's sourcing specifically: is this an unsupported
   assertion dressed as fact, an overstated certainty (a retrieval hit restated as proof, a
   "survived" verdict restated as "verified" — the honest-ceiling failure mode), or a link that
   was never actually confirmed to resolve to, and support, the claim attributed to it?
2. **Hand off the same draft to `@conflict-auditor`.** Check it against this project's own
   already-established findings (a prior verdict on the same claim, a source rating already on
   record), and for internal contradictions within the summary itself.
3. **A finding on any specific claim means that claim is not ready to present.** Revise it —
   re-fetch, re-verify, correct the citation, hedge the wording, or drop it as an explicitly
   unresolved finding per the producing agent's own honest-ceiling rules — then **re-run both
   audits against the revised claim.** This is a loop: keep revising and re-auditing until a
   clean pass, not a one-shot check.
4. **Escalation valve, precisely scoped per claim.** Track failures **per claim**, identified by
   the claim's stable underlying assertion — what is actually being claimed — never by the
   URL/citation attached to it. A citation can be swapped out between cycles while the real,
   unsupported assertion underneath it persists unchanged; tracking by URL would let exactly that
   case dodge escalation forever. If the **same claim** still has an open finding after **3
   consecutive revise-and-reaudit cycles**, or a finding can't be resolved because a required
   verification path doesn't exist in this project yet (e.g. `agentteams.research.verify`'s
   `extract_claims`/`audit_claims` need a chat-completion integration this project hasn't wired
   up), stop looping on that claim specifically. Report it as an explicit, unresolved, escalated
   finding — never silently dropped, never asserted as true by default — and escalate to
   `@orchestrator`/the user.
5. **Escalating one claim does not block the rest of the summary.** Any other claim that
   independently passed the gate may still be presented. Only the escalated claim is called out
   as unresolved rather than presented as settled — this mirrors the same "never silently drop an
   unresolved finding, but don't let one unresolved item block everything that did check out"
   balance this project's other honest-ceiling rules already strike.
6. **Only a clean pass, or an explicit per-claim escalation, ends the task.** Presenting a summary
   that never went through steps 1-2 at all is the specific failure mode this reference exists to
   close.

## Worked example: a citation that keeps failing the same way

A research task cites `https://example-blog.net/2026/some-library-v3-migration` for the claim
"library X's v3 release removed the legacy `Config` class." Cycle 1: `@adversarial` flags that
the domain isn't in this project's reputable-source allowlist and the page is a third-party blog
post, not the library's own changelog or release notes — sourcing tier too weak for a factual
removal claim. Revision: search again, find the library's own GitHub releases page, re-cite from
there. Cycle 2: `@adversarial` now flags that the *new* citation is real and reputable, but the
release notes actually say `Config` was *deprecated*, not *removed* — the claim itself
overstates what the source says. Revision: correct the claim's wording to match the source
precisely ("deprecated, scheduled for removal in a future release" — not "removed"). Cycle 3:
clean pass from both audits. Note what happened across the three cycles: the *citation* changed
between cycles 1 and 2, but the thing being tracked for escalation purposes — "is `Config`'s
removal-status claim resolved?" — is the same claim throughout, which is exactly why step 4
above tracks by assertion, not by URL: had cycle 2's fix been graded as "a new claim"
because it carried a new link, a persistently-wrong assertion could swap sources indefinitely and
never trip the escalation valve meant to catch it.
<!-- AGENTTEAMS:END content -->
