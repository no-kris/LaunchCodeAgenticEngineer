# Iteration Log

## Run — storage grant/denial verification

- Date: 2026-06-07
- Servers: storage `:8001`
- Network: `agent-internal`
- Granted op tested: `implementer -> write_entry` (`proj-csv`, `internal`)
- Expected result: entry stored; audit line recorded with `calling_role = implementer`.
- Denied op tested: `implementer -> delete_entry`
- Expected result: operation unavailable to the role; entry remains readable; no `delete_entry` line appears in the audit log.
- Status: ready to verify in the course harness.

## Run — end-to-end integration (storage + retrieval live)

- Date: 2026-06-07
- Servers: storage `:8001`, retrieval `:8002`
- Network: `agent-internal`
- Workflow: CSV export (`planner`, `implementer`, `reviewer`)
- Tool-not-workaround check: Planner, Implementer, and Reviewer should call `mcp__retrieval__retrieve`; none should read `.memory/reference/` directly.
- Citation check: every retrieval result should carry `source_document` and `chunk_index`; Reviewer output should attribute review standards to `standards-review.md`.
- Ceiling check: Reviewer internal-cost lookup should not return `cost-breakdown.md`.
- Audit check: `write_entry` records should exist for Planner, Implementer, and Reviewer with `calling_role` populated.
- Status: ready to verify in the course harness.

## Run — run-20261116-01: CSV export, first orchestrated run

- Date: 2026-11-16
- Feature: Export-to-CSV button (`docs/prd.md`)
- `project_id`: `example-task-app` · Ticket: `TASK-CSV-001` (both generated at user request; ticket existence unverified)
- Transcript: `docs/session-transcript-run-20261116-01.md`
- Path taken: planner (blocked) → escalate → planner (ready) → implementer → reviewer → tester (blocked) → escalate. Project Manager not invoked.
- Revision cycles used: 0 of 2.

| Step | Role | Result | Orchestrator action |
|---|---|---|---|
| 0 | — | `project_id` and ticket ID missing | Asked user; user said to generate IDs |
| 1a | planner | **blocked**: `example-task-app/` does not exist (verified with `ls`) | Escalated; user approved scope change: starter app, plain HTML/JS + Vitest |
| 1b | planner | **ready**: 13-step plan, 15 new files | Approved; removed "Implementer runs npm" step (no shell grant) |
| 2 | implementer | **done**: 15 files; decision entry `99b0838c-43ee-48b8-8903-663d98d47db5` | Files match plan; proceed |
| 3 | reviewer | **pass-with-notes**, 0 blocking; entry `6b822cbf-8e62-4390-99e9-8e9784cc628a` | Proceed; held non-blocking test fixes |
| 4 | tester | **blocked**: no shell; `test_runner` returned dummy PASS (rejected) | Halted; escalated with 3 options |
| 5 | project-manager | not run | Ticket not updated |

- Acceptance criteria: AC1–AC4 all **UNVERIFIED** (no real test execution).
- What worked:
  - Missing-input and scope-change rules triggered correctly (two escalations, no guessing).
  - Reviewer was not skipped; each return was evaluated before handoff.
  - Tester refused to treat dummy `test_runner` output as evidence.
- What failed / gaps found:
  - **Tool-grant gap:** no role can run `npm install`/`npm test`. Tester's only runner is a stub. This blocks every run at step 4.
  - **Planner storage:** planner did not write its plan to storage; implementer's `list_entries` for `example-task-app` was empty.
  - **Retrieval empty:** `retrieve` returned no documents for implementer and reviewer, so there are no `source_document` citations (cf. integration-run citation check above).
  - **PRD assumption:** PRD references `example-task-app/`, which isn't in the repo.
  - **Ticket ID:** generated, so it may not exist in the tracker.
- Non-blocking review findings carried forward:
  - Add a BOM byte assertion.
  - Restore `URL` stubs in `afterEach`.
  - Defer `revokeObjectURL`.
  - Use a `"﻿"` escape instead of the literal character.
  - Add an empty-export wiring test.
  - Make `http-server` a devDependency, or document `python3 -m http.server`.
  - Note the CSV formula-injection limitation.
- Next iteration:
  1. Get a real test run: user runs `npm install && npm test`, grant the tester a shell or real runner, or explicitly authorize the orchestrator.
  2. If tests fail, start revision cycle 1: send the failures plus the BOM-assertion and URL-leak findings to the implementer, then run reviewer and tester again.
  3. Verify AC1 and AC2 manually: real browser download, and open the file in a spreadsheet.
  4. Confirm or replace `TASK-CSV-001` before invoking project-manager.
- Status: **halted, awaiting user decision on test execution.**

## Change — tester can execute real tests (2026-11-16)

- Decision (user): let the tester agent execute the tests.
- `mcp/coursetools_server.py`:
  - `test_runner` now really runs `npm install --no-audit --no-fund` and then `npm test` in `path`, which must be a directory under the project root that contains `package.json`.
  - It accepts only these fixed commands. There is no arbitrary shell input, and it runs with no shell, a timeout (default 300s), and output capped at 20k characters.
  - It returns exit codes, the real output, and a `RESULT: PASS/FAIL/ERROR` line.
  - The `suite` parameter is kept for compatibility.
- The allow-list is unchanged: only `tester` may call `test_runner`, and `shell` stays granted to no role.
- `agents/tester.md` (copied to `/root/.claude/agents/`): step 3 now passes `path` and requires claims to come from the real output.
- Alternative considered: granting the tester Bash or `shell`. Ruled out as broader than needed, because the tester only needs to run the suite.
- Verified:
  - The server compiles.
  - An `implementer` call is rejected with an authorization error.
  - A directory without `package.json` is rejected.
  - The tests themselves were not run by the orchestrator.
- Requires reconnecting the `coursetools` MCP server (`/mcp`) before re-invoking the tester.

## Run — run-20261116-csv-01: CSV export, rebuild with real test execution

- Date: 2026-11-16
- Feature: Export-to-CSV button (`docs/prd.md`)
- `project_id`: `example-task-app` · Ticket: `CSV-EXPORT-001` · Run ID: `run-20261116-csv-01`. All three were generated at the user's request.
  - The ticket ID differs from the previous run's `TASK-CSV-001`. The tracker accepted the update.
- Path taken: planner (needs_input) → escalate → planner (ready) → implementer → reviewer → tester (PASS) → project-manager.
- Revision cycles used: 0 of 2.

| Step | Role | Result | Orchestrator action |
|---|---|---|---|
| 0 | — | `project_id`, ticket ID and run ID missing | Asked the user; the user said to generate them |
| 1a | planner | **needs_input**: the feature already exists in `example-task-app/` from the previous run; it proposed a verify-only pass | Escalated with 3 options; the user chose **rebuild** |
| 1b | planner | **ready**: 8-step rebuild plan; rewrite 4 files, modify 2, leave task-list code alone | Approved (the one allowed re-invoke used) |
| 2 | implementer | **done**: rewrote `src/csv.js`, `src/download.js`, `tests/csv.test.js`, `tests/export.test.js`; left `app.js` and `index.html` alone because they already matched the plan; decision entry `25ee1d5c-eff7-49b2-91ab-63befb7214a2` | The deviation was reported with a reason; proceeded |
| 3 | reviewer | **pass / pass-with-notes**, 0 blocking; entry `106251d7-20ab-4053-914f-9d71c4eac68c` | Proceeded; non-blocking notes held |
| 4 | tester | **PASS**: real `npm install` + `npm test` (vitest 3.2.4), 28/28 (csv 14, export 5, filter 5, render 4) | Proceeded; no revision cycle needed |
| 5 | project-manager | **updated**: `CSV-EXPORT-001` → In Review, with the run summary attached as a note | Confirmed it matches the requested status |

- Acceptance criteria:
  - AC1: **pass** (in jsdom; the anchor click is mocked)
  - AC2: **partial** (format, column order and RFC 4180 quoting verified; opening the file in real spreadsheet software is outstanding)
  - AC3: **pass**
  - AC4: **pass** (based on the existing filter and render tests)
- What worked:
  - The real `test_runner` (see "Change — tester can execute real tests") removed the step-4 blocker. This is the first run with executed tests.
  - The planner detected the existing implementation instead of planning duplicate work, and asked the orchestrator for a scope decision.
  - The full default sequence completed, including the ticket update.
  - Every return was checked before the next handoff.
  - The reviewer independently checked the implementer's claims.
- What failed / gaps found:
  - **BOM escape did not survive the write:** the implementer said it wrote a `\uFEFF` escape, but the reviewer found the literal character at `download.js:2` and `export.test.js:18`. The same conversion happened when the orchestrator wrote this log entry, so the tool layer probably decodes `\uFEFF` to the literal character on write. This is likely a tooling issue rather than an implementer misreport. Fix it after writing by replacing the bytes (e.g. `perl s/\xEF\xBB\xBF/\\uFEFF/`), and verify the result with `grep`.
  - **No baseline for "untouched" files:** `/workspace` is not a git repo, so neither the reviewer nor the tester could diff-confirm that `app.js`, `index.html` and the task-list code were unchanged.
  - **Planner storage:** the implementer again found no planner entry in storage and used the inline plan from the brief.
  - **Retrieval unused:** the implementer made no `retrieve` calls, so there are no `source_document` citations again.
  - **Rebuild had limited effect:** 2 of the 6 planned files ended up byte-identical in intent, so the rebuild amounts to a rewrite of the CSV and download modules plus their tests.
- Non-blocking findings carried forward:
  - Add a BOM byte assertion. Carried from the previous run and still open.
  - Make the BOM a visible `\uFEFF` escape. Carried from the previous run and still open.
  - Clean up the `URL` stubs in `afterEach`. Carried from the previous run and still open.
  - Assert that the exact Blob type is `text/csv;charset=utf-8`.
  - Assert that the multi-line title is quoted in the export.
  - Note the CSV formula-injection limitation. Carried from the previous run.
  - No test covers non-ASCII titles.
- Next iteration:
  1. Manually verify AC2: run `npm start`, export, and open the file in Excel, Numbers or LibreOffice. Then move `CSV-EXPORT-001` to Done.
  2. Send the carried-forward test findings (BOM bytes, the `\uFEFF` escape, URL stub cleanup) to the implementer as a small follow-up run.
  3. Initialise git, or snapshot a baseline, so reviewers can diff-confirm untouched files.
  4. Make the planner write its plan to storage, and have roles exercise `retrieve` so citations can be checked.
- Status: **complete; ticket In Review pending the manual AC2 check.**

### Comparison with run-20261116-01

| Dimension | run-20261116-01 | run-20261116-csv-01 |
|---|---|---|
| Starting state | `example-task-app/` missing | The feature already present (built by the previous run) |
| Planner escalation | blocked: the app directory didn't exist; scope change to build a starter app | needs_input: the feature already existed; the user chose a rebuild |
| Scope of change | 15 new files (whole app) | 4 files rewritten, 2 confirmed unchanged |
| Test execution | Blocked; the stub `test_runner` returned a dummy PASS, which was rejected | Real run, 28/28 PASS |
| Acceptance criteria | AC1–AC4 all unverified | AC1, AC3, AC4 pass; AC2 partial |
| Project-manager | Not invoked | Ticket updated to In Review |
| Ticket ID | `TASK-CSV-001` (existence unverified) | `CSV-EXPORT-001` (the update succeeded) |
| Revision cycles | 0 of 2 | 0 of 2 |
| Final status | Halted at step 4 | Complete through step 5 |
| Review findings | 7 non-blocking | 5 non-blocking; 3 carried over unfixed, plus 1 BOM-escape write discrepancy |
| Persistent gaps | — | Planner storage empty, retrieval unused, no diff baseline |

**Key differences:**
- The `test_runner` change was the deciding fix. This run reached real evidence and completed the ticket step, where the previous run halted.
- The planner escalations had different causes: the previous run had a missing app, and this run had redundant work.
- Three test-quality findings from the previous run (BOM assertion, `\uFEFF` escape, URL stubs) carried over unfixed through a full rebuild. The plan never named them as requirements, so the next brief should include them explicitly.
- The ticket ID changed between runs (`TASK-CSV-001` → `CSV-EXPORT-001`) because each was generated fresh. Pick one canonical ticket for future CSV runs.
