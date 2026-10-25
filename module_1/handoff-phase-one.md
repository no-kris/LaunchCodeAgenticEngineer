HANDOFF DOCUMENT

Overall Task

The user is revising a short technical blog post, "Getting Started with API Integration," over several rounds. In each round, the agent edits exactly one section, as the user directs, and applies a fixed seven-rule style guide. The goal is a post written in active voice with short sentences, banned words removed, technical terms bolded, a summary sentence ending each section, and Oxford commas throughout. The user reviews each section before the next one starts.

Phase One Summary

- Round 0: The user shared the style guide and the blog post and asked for confirmation only, with no edits. The agent confirmed it had read both. It proposed a working list of technical terms to bold (see Gotchas), and the user didn't object.
- Round 1: The agent edited the Introduction only. The user approved it ("Good.").
- Round 2: The agent edited the Authentication section only. The user approved it ("Good.") by invoking this handoff.
- Untouched: Making Requests and Error Handling still contain the original text.
- Process: The user never sent instructions for the next round after approving Authentication. Phase two should wait for the user to direct each section.

Current State of All Artifacts

Blog post title: Getting Started with API Integration

Introduction (EDITED and APPROVED. Do not change.)

Developers use APIs to connect different software systems together. When you use an API, you send a request to a remote server and wait for it to respond. Your application can then process that response however it needs.

In short: APIs let your application send requests to remote servers and act on their responses.

Authentication (EDITED and APPROVED. Do not change.)

Most APIs require authentication, usually through API keys or tokens. Your application sends these credentials with each request. The server validates them before it responds. If you provide invalid credentials, the server returns a 401 error.

In short: Send valid credentials with every request, or the server will reject it with a 401 error.

Making Requests (ORIGINAL, not yet edited)

HTTP requests are made using methods like GET, POST, PUT, and DELETE. A GET request is used when data needs to be retrieved, while POST is utilized when new data needs to be created on the server. The response that is returned will include a status code, headers, and usually a body containing JSON data that can then be parsed.

Error Handling (ORIGINAL, not yet edited)

Errors in API integrations are often caused by network issues, invalid input, or rate limiting applied by the provider. It is recommended that retry logic be implemented with exponential backoff for transient errors. Permanent errors, such as 404 or 400 responses, should be surfaced to the user rather than retried.

Rules and Constraints in Effect

STYLE GUIDE (apply to all edits):

- Never use passive voice. Always rewrite passive constructions as active voice.
- Sentences must be 25 words or fewer. Split any longer sentence into two.
- Never use the word "utilize" -- replace it with "use"
- Never use the word "leverage" -- replace it with "use" or "build on"
- Technical terms must be bolded on first use in each section
- Every section must end with a one-sentence summary starting with "In short:"
- Oxford comma required in all lists

Scope rule (from the user's per-round instructions): Each round's instruction follows the pattern "Now edit only the [X] section. Apply the full style guide." Edit only the section named. Leave every other section exactly as it is.

Project rule (from /workspace/CLAUDE.md): At the start of each new phase, before any editing or analysis, do five things. Restate the task goal in one sentence. List the rules currently in effect verbatim. State which prior rules are no longer in effect. Identify the artifact being worked on. Then proceed.

Phase Two Instructions

1. Wait for the user's next instruction. The likely next request is "Now edit only the Making Requests section. Apply the full style guide," but don't assume it.
2. Before editing, run the CLAUDE.md context boundary procedure.
3. Edit only the named section. Rewrite every passive construction in active voice. Replace "utilize" or "utilized" with "use." Keep every sentence at 25 words or fewer. Bold technical terms on first use within that section. Check that every list has an Oxford comma. End the section with one "In short:" sentence that also follows every rule.
4. Present the revised section. Then list the changes, and state that the other sections are unchanged.
5. Wait for the user's approval ("Good.") before going on to the next section. Error Handling is probably last.
6. Never re-edit the approved Introduction or Authentication sections unless the user explicitly asks.

Acceptance Criteria for Phase Two

The original task never stated explicit acceptance criteria. The closest verbatim requirement is the user's own wording, "every edit you make must follow these rules," along with the style guide above. In practice, a section is done when all of these are true:
- It has zero passive constructions.
- Every sentence is 25 words or fewer.
- It contains no "utilize" and no "leverage."
- Technical terms are bolded on first use in that section.
- Every list uses an Oxford comma.
- It ends with exactly one "In short:" sentence.
- No other section changed.
- The user approved it.

Known Constraints and Gotchas

- Bolding resets per section. A term already bolded in an earlier section gets bolded again on its first use in a new section. For example, APIs is bolded in both the Introduction and Authentication. Bold only the first use within a section.
- Agreed technical term list. The user didn't object to this list: API, authentication, API keys, tokens, 401/404/400 errors, HTTP, the method names (GET, POST, PUT, DELETE), status code, headers, JSON, retry logic, exponential backoff, and rate limiting. Precedent so far: "request," "response," and "remote server" were not bolded.
- Making Requests pitfalls:
  - It has three passive constructions: "are made using," "is used when data needs to be retrieved," and "needs to be created."
  - "utilized" appears in the second sentence.
  - The third sentence uses "is returned" and "can then be parsed."
  - Its two lists ("GET, POST, PUT, and DELETE" and "a status code, headers, and usually a body") already have Oxford commas. Keep them.
- Error Handling pitfalls:
  - It has three passive constructions: "are often caused by," "be implemented," and "should be surfaced."
  - "It is recommended that…" is also passive. Rewrite it with an actor, for example "Implement…" or "We recommend…"
  - "rate limiting applied by the provider" is a passive participle phrase. Rewrite it, for example as "rate limits that the provider enforces."
  - The list "network issues, invalid input, or rate limiting" already has an Oxford comma.
- The "In short:" sentence follows every rule too: active voice, 25 words or fewer, and no bolding needed if the term already appeared in bold earlier in that section.
- Whitespace: The original post was hard-wrapped mid-sentence. The text above joins those lines into paragraphs, with no wording changes.
- Minor prior choices: The agent removed filler words as part of active-voice rewrites, such as "essentially" from the Introduction. The user accepted this. Keep such cuts small, and don't change meaning.

---

Please check this for completeness and accuracy before you close the session. In particular, the Acceptance Criteria section says plainly that the original task never stated any, so I wrote criteria based on the style guide instead of inventing a quote. Edit it if you have stricter criteria in mind. I can also save it as a file if that's easier to hand to the next session.
