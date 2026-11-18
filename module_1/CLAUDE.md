# Agent Context Boundary Policy

## Purpose
This file defines how context boundaries are managed in this project.
At the start of each new phase of work, the agent must follow the
procedure below before taking any action.

## Context Boundary Procedure
At the start of each new phase, before doing any editing or analysis:

1. Restate the current task goal in one sentence.
2. List the rules currently in effect (verbatim, not paraphrased).
3. State explicitly which prior rules are no longer in effect, if any.
4. Identify the specific artifact being worked on in this phase.
5. Then proceed with the requested work.

## Why This Matters
Rules and requirements change during long sessions. This procedure ensures the agent is always operating from the current version of the rules, not a prior version buried in conversation history.

## Compaction Policy

Compaction is a last resort. Proactive summarization (see .claude/skills/summarize-session/SKILL.md) should be triggered before the context window exceeds 60% capacity to avoid relying on compaction.

Observations from testing (update this based on your own runs):
- Compaction reliably preserves: [fill in based on your probe results]
- Compaction may lose or distort: [fill in based on your probe results]
- Manual compaction should be triggered at: [fill in your threshold]
Fill in the bracketed sections based on your actual probe results.

## Automated Summarization Trigger

### How to Monitor Context Usage

Claude Code displays token usage after each response. It appears as:

Tokens: [used] / [limit] ([percentage]%)

After every response you generate, check this value. You do not need

to report it unless the threshold below is crossed.

### Threshold

When context usage reaches or exceeds 60% of the context window

limit, you must do the following before responding to the next

user message:

1. Pause and notify the user:

 "Context window is at [X]%. Triggering automatic summarization

 before continuing."

2. Invoke the summarization skill internally, producing a full

 session summary in the format defined in

 .claude/skills/summarize-session

3. Present the summary to the user and ask them to confirm it is

 accurate before proceeding.

4. Once the user confirms the summary, continue with the original

 task.

### Why 60%

60% leaves sufficient headroom for the summarization turn itself

(which generates substantial output) without risking automatic

compaction firing mid-summary. Adjust this threshold in the version

history below if your workflow data supports a different value.

### Override

If the user explicitly says "skip summarization" or "continue without

summarizing", respect that instruction for the current turn only.

The trigger resets on the next turn.
