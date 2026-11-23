# Ground-Truth Retrieval Run — 2026-11-23

Script: `mcp/retrieval/run_ground_truth.py`
Server: `retrieval` MCP server (`mcp/retrieval/server.py`), default chunking (`paragraph`), `http://localhost:8002/mcp`
Cases: see `docs/retrieval-ground-truth.md`

## Result

**7 / 8 passed (87.5%)** — above the 80% floor, so the script exited 0.

| ID | Kind | Expected doc | Verdict | Top hit(s) |
|----|------|---------------|---------|------------|
| Q1 | precision | `decision-csv-format.md` | PASS | `decision-csv-format.md#0` (vector, 0.759) |
| Q2 | precision | `feature-csv-export.md` | PASS | `feature-csv-export.md#0` (vector, 0.682) |
| Q3 | keyword | `error-codes.md` | PASS | `error-codes.md#2` (vector, 0.779), `#0` (0.656), `#3` (0.65) |
| Q4 | precision | `feature-csv-export.md` | PASS | `feature-csv-export.md#1` (vector, 0.843) |
| Q5 | ceiling | forbidden: `cost-breakdown.md` | PASS | `decision-csv-format.md`, `feature-csv-import.md`, `error-codes.md` (all keyword) — forbidden doc absent |
| Q6 | precision | `standards-review.md` | PASS | `standards-review.md#0` (vector, 0.866) |
| Q7 | precision | `security-export-visibility.md` | PASS | `security-export-visibility.md#0` (vector, 0.761), `decision-csv-format.md#0` (vector, 0.702) |
| Q8 | precision | `api-spreadsheet-library.md` | **FAIL** | `api-spreadsheet-library.md#1,#0,#2` (all **keyword**, no score) |

## Failure analysis — Q8

Query: *"Which spreadsheet library do we use to generate exports?"*

The correct document (`api-spreadsheet-library.md`) was returned, but only through the **keyword fallback** path — the vector search found no chunk from that document with `similarity_score >= 0.65`, so `retrieve()` fell through to FTS5 keyword search, which returns `similarity_score: None`.

Q8 is a `precision`-kind case in `run_ground_truth.py`, and `judge()` requires a vector hit (`similarity_score >= 0.65`) for that kind — a keyword-only hit does not satisfy it, regardless of whether the right document was found. This is a semantic-similarity gap between the query phrasing and the document's chunk content under the current embedding model/chunking (paragraph chunking, `all-MiniLM-L6-v2`), not a bug in the ceiling/filter/project logic.

## Notes

- All other precision cases cleared the 0.65 vector threshold comfortably (0.68–0.87).
- The ceiling case (Q5) correctly withheld the `confidential`-classified `cost-breakdown.md` document.
- Overall pass rate (87.5%) clears the script's 80% floor, so no `SystemExit` was raised.
