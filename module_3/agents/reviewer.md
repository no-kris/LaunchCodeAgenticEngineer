---
name: reviewer
description: >
 Reads the Implementer's changes and reports problems (bugs, missing tests,
 unclear ownership, risky edits). Read-only. Proposes changes; never makes
 them. Invoked after the Implementer.
model: sonnet
tools:
 - file-read
 - codebase-search
disallowedTools:
 - file-write
 - shell
 - test-runner
 - task-tracker
 - web-search
autonomy: high
version: 1.1.0
---
