# 1. Quality Rubric

## 1.1 Dimensions

### 1.1.1 Build Result Accuracy

Measures whether the agent correctly identified the final outcome of the Docker build. A high score requires the stated result, success or failure, to match the actual exit status of the build command.

### 1.1.2 The summary includes warnings and errors present in the build output; it does not omit any.

This dimension measure whether the agent inluded any warning and errors it recieved after running the repo's Docker build command.

### 1.1.3 The recommendation is consistent with the build result.

This dimensions measures whether the agent's proceeding recommendation aligns with the Docker build result it recieved.

Alternatives considered: Whether the agent attempted to fix any errors it encountered. Ruled out because the results align more with binary pass/fail.
