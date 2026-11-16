# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Docker-based development environment for LaunchCode's **Agentic Programming** course, Module 3. 

## MCP Servers

Two MCP servers are pre-installed and configured in `/root/.claude/settings.json`:

### Slack
- Package: `@modelcontextprotocol/server-slack`
- Requires env vars: `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID`
- Allows Claude Code prompts to read channels, post messages, and interact with Slack workspaces.

### Gmail
- Package: `@gongrzhe/server-gmail-autoauth-mcp`
- OAuth credentials stored in `/root/.gmail-mcp/` (persist this directory across container runs if needed)
- Allows Claude Code prompts to read, search, and send Gmail messages.

## Skills

Pre-configured skills (invoked with `/skill-name` in Claude Code):

| Skill | Description |
|---|---|
| `/send-slack-message` | Send a message to a Slack channel |
| `/check-gmail` | Summarize recent unread Gmail messages |
| `/send-email` | Draft and send an email via Gmail |
| `/summarize-session` | Bullet-point summary of the current session |

Skills are defined in `settings.json` which is copied to `/root/.claude/settings.json` during image build.

## Agents

Pre-configured sub-agents available inside Claude Code sessions. Agents are autonomous specialists that Claude Code can invoke automatically or that you can request explicitly.

| Agent | Description |
|---|---|
| `code-reviewer` | Reviews recent git changes for quality, security, and maintainability |
| `email-summarize` | Checks new Gmail messages and posts sender + 2-line summary to #test Slack channel |

Agents are defined as Markdown files with YAML frontmatter in `/root/.claude/agents/` inside the container. Source files live in the `agents/` directory of this repo and are copied in at build time.

**Running an agent:**

Ask Claude Code to use the agent explicitly:
```
Review my recent changes using the code-reviewer agent.
```

Or Claude Code may invoke it automatically when the task matches the agent's description.

## Running Streamlit Apps

From inside the container:
```bash
streamlit run app.py
```

Access at `http://localhost:8501`.

## Key Dependencies (requirements.txt)

- `anthropic` — Claude API client
- `streamlit` — web UI framework
- `python-dotenv` — environment variable management
- `slack_sdk` — Slack integration (Python)
- `google-api-python-client`, `google-auth-oauthlib` — Gmail/Google API access (Python)
- `fastapi`, `flask`, `uvicorn` — web frameworks
- `pydantic`, `httpx` — HTTP and data validation

## Environment & Tools in the Container

- Python 3.12 (aliased as `python` and `pip`)
- Claude Code CLI (`claude`) installed globally via npm
- OpenCode (`opencode-ai`) installed globally via npm
- MCP server: `@modelcontextprotocol/server-slack`
- MCP server: `@gongrzhe/server-gmail-autoauth-mcp`
- ngrok for tunneling
- Workspace mounted at `/workspace`

## Gmail API Setup

Place `credentials.json` (from Google Cloud Console) in your workspace directory. On first run it triggers OAuth and saves `token.json`. Both files should be in `.gitignore`.

## Orchestrator workflow instructions

You are the parent/orchestrator for the Module 3 workflow. You do not write
code, review changes, run tests, or update tickets yourself. You sequence the
specialist agents, evaluate what each one returns, decide whether to loop, skip,
or escalate, and assemble the final run summary.

### Inputs required before the first handoff

Collect and confirm:

- The feature request or the path to `docs/prd.md`
- The repository path
- `project_id`
- The ticket ID
- Acceptance criteria
- An optional run ID

If any required input is missing or ambiguous, stop and ask the user. Do not
guess, and do not delegate the ambiguity to a subagent.

### Default sequence

| Step | Agent | Handoff contains | Expected return | On failure |
|---|---|---|---|---|
| 1 | `planner` | Feature request + repository path | Numbered plan + file list | Re-invoke once with clarifying notes; then escalate |
| 2 | `implementer` | Plan + file list + `project_id` + acceptance criteria | Modified files + recorded decisions | Invoke `researcher` for an external-documentation blocker; otherwise escalate |
| 3 | `reviewer` | Plan + modified files + implementer summary | Review report with a verdict per section | Return blocking findings to `implementer`, then re-run `reviewer` |
| 4 | `tester` | Modified files + acceptance criteria | Test report with pass/fail per criterion | Return failures to `implementer`, then re-run `reviewer` and `tester` |
| 5 | `project-manager` | Assembled run summary | Ticket update confirmation | Report the failure to the user and escalate |

Do not skip the `planner` unless the user supplies an approved plan and file
list. Do not skip the `reviewer` for any implementation output. Do not skip the
`tester` unless the user explicitly waives testing.

### Evaluate each return before continuing

- **Plan:** numbered, ordered, complete file list, and no open question that
  blocks implementation.
- **Implementation:** modified files match the plan, decisions are reported,
  and no denied tool was used.
- **Review:** explicit verdict per section, with actionable findings.
- **Tests:** overall pass/fail and coverage of every acceptance criterion.
- **Ticket:** confirmation matches the requested status.

If a subagent returns `blocked` or `needs_input`, do not continue down the
default path. Resolve the blocker or escalate.

### Optional researcher branch

Invoke the `researcher` only when another role raises an external-documentation
blocker:

1. The blocked role returns the blocker to you.
2. Send the `researcher` one narrow question plus the minimum context needed to
   answer it.
3. Pass the findings back to the blocked role, normally the `implementer`.
4. The `researcher` never edits code and never calls another role.

### Loop, skip, and escalation rules

- Allow at most **two revision cycles** per run. A revision cycle is one
  `implementer` revision followed by another `reviewer` and `tester` pass.
- After two cycles without a clean review and passing tests, stop and escalate
  to the human.
- Escalate immediately for:
  - conflicting reviewer verdicts on the same section,
  - missing or ambiguous inputs,
  - tool authorization errors,
  - ticket update failures,
  - scope changes that require user approval,
  - any subagent that remains blocked after one resolution attempt.
- Pass only the fields the next role needs. Never pass the full session history
  or another role's private reasoning.
- Attribute retrieved claims to their `source_document` when summarising them.
