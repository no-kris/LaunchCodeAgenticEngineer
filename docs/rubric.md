# 1. Quality Rubric

## 1.1 Dimensions

### 1.1.1 Build Result Accuracy

Measures whether the agent correctly identified the final outcome of the Docker build. A high score requires the stated result, success or failure, to match the actual exit status of the build command.

## Scoring Guide

1. Does not meet - The agent does not report the build outcome or reports a misleading build outcome.

Level 1 example: “The Docker build ran.” The build actually failed with exit code 1. No pass/fail is stated, and the wording implies success — a misleading outcome.

2. Partially meets - The agent reports the build outcome with missing context - e.g. says, "the build had issues" without describing the issues or reporting pass/fail.

Level 2 example: Agent output reads: “The build had issues.” The agent neither reports pass/fail nor says the build failed, leaving the outcome ambiguous.

3. Meets - The agent correctly reports whether the Docker build passed or failed.

Level 3 example: Agent output reads: “The Docker build failed.” The build exited with code 1 — the stated result is correct, though no supporting evidence is given.

4. Exceeds - The agent correctly reports whether the Docker build passed or failed and includes supporting evidence such as the exit code or final line of the build output.

Level 4 example: Agent output reads: “The Docker build failed (exit code 1); the final log line was ERROR: failed to solve: base image tag is required.” Stated result matches and is backed by the exit code and final output line.

### 1.1.2 The summary includes warnings and errors present in the build output; it does not omit any.

This dimension measure whether the agent inluded any warning and errors it recieved after running the repo's Docker build command.

## Scoring Guide

1. Does not meet - The agent omits one or more errors that appeared in the build output summary. A reviewer would have an incomplete or misleading picture of what went wrong.

Level 1 example: Agent output reads: “The build encountered some issues and did not complete successfully.” The build log contained three distinct errors. None are named in the summary.

2. Partially meets - The agent captures all errors, but misses one or more warnings. The summary is not misleading, but it is incomplete.

Level 2 example: Agent output reads: “The build failed with the following errors: missing base image tag, undefined build argument NODE_ENV. No warnings were reported.” The build log contained those two errors plus a deprecation warning for a legacy COPY syntax. The warning is absent from the summary.

3. Meets - The agent captures all errors and warnings present in the build output. The summary is sufficient at providing an accurate picture of the build output.

Level 3 example: Agent output reads: “The build failed with two errors (missing base image tag, undefined build argument NODE_ENV) and one warning (deprecated COPY syntax on line 12).” All items from the build log are present.

4. Exceeds - The agent captures all errors and warnings present in the build output. The agent groups or prioritizes the most critical errors first without requiring the reviewer to read the full summary.

Level 4 example: Agent output reads: “The build failed. Two errors must be resolved before the image can build: a missing base image tag (blocking) and an undefined build argument NODE_ENV (blocking). One non-blocking warning is present: deprecated COPY syntax on line 12, which will become an error in Docker 26.” Errors and warnings are separated, labeled by severity, and the warning includes forward-looking context.

### 1.1.3 The recommendation is consistent with the build result.

This dimensions measures whether the agent's proceeding recommendation aligns with the Docker build result it recieved.

## Scoring Guide

1. Does not meet - The agent does not give a recommendation or gives a misleading one - e.g. recommends proceeding after a failed build.

Level 1 example: Agent output reads: “The build failed, but the image should still be usable — go ahead and deploy.” A failed build means the image was not produced, so proceeding is wrong.

2. Partially meets - The agent provides a recommendation, but does not provide supporting evidence and is too vague.

Level 2 example: Agent output reads: “I’d hold off for now.” The direction is plausible for a failed build, but no reason or evidence is given.

3. Meets - The agent provides a recommendation that accurately represents the build result.

Level 3 example: Agent output reads: “Since the build failed, do not proceed until the missing base image tag and undefined NODE_ENV are resolved.” The recommendation matches the failed result.

4. Exceeds - The agent provides a recommendation that accurately represents the build result and provides supporting evidence. The agent provides next steps following the build result.

Level 4 example: Agent output reads: “Because the build failed (exit code 1), the image cannot be used. Next steps: add the base image tag, define NODE_ENV, then re-run the build.” The result is backed by evidence and includes concrete next steps.

Alternatives considered: Whether the agent attempted to fix any errors it encountered. Ruled out because the results align more with binary pass/fail.

## Pass Threshold
A run is passing if it scores 3 or higher on all dimensions.

Reasoning: Build Result Accuracy and Recommendation Consistency must both be correct for the output to be trustworthy. A run that scores 4 on coverage, but 2 on accuracy produces a well-documented wrong answer, which is worse than a sparse correct one. A dimension floor prevents high scores on secondary dimensions from masking failures on primary ones.

## Notes on Threshold Design

Considered an aggregate minimum of 8/12 instead of a dimension floor. Ruled out because it would allow a run scoring 1 on Build Result Accuracy to pass if it scored 4 on all other dimensions. An agent that reports the wrong build result is not acceptable, regardless of how well it covers warnings. The dimension floor prevents that outcome.
