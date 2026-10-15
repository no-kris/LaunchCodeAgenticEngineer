This workflow reviews this project's Docker setup by running the documented build command in the README file, reviewing the outcome, and reporting whether the repo is ready.

Trigger: A developer invokes Claude by giving a task prompt from the repository root.

If the Docker build succeeds, the agent reports any warnings and recommends proceeding.

If the Docker build fails, the agent reports the error and recommends against proceeding. The agent does NOT attempt to fix the error.

1. Read the repository’s documentation to identify the documented Docker build
command.

2. Run the Docker build command inside the sandbox.

3. Capture the output from the build process.

4. Evaluate the build result (success or failure).

5. Summarize any warnings or errors present in the output.

6. Produce a final recommendation, ready to proceed or not ready, with a brief
rationale

The agent correctly identifies whether the Docker image was built successfully or failed.

The agent does not attempt to fix any errors.

The agent did not push, publish, or deploy anything.
